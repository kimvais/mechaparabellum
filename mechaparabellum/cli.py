import enum
import logging
import math
import pathlib
import re
import json
from collections import Counter, defaultdict
import datetime
from operator import itemgetter

import platformdirs
from packaging.version import InvalidVersion, Version

from rich.console import Console
import rich.table
import fire
import requests

from mechaparabellum.utils import get_newest
from mechaparabellum.units import Unit

AUTHOR = 'kimvais'
APP_NAME = 'mechaparabellum'
NUMBER_OF_FORMATION_FILES = 10

GAME_START_RE = re.compile(r'^\[C] recv message \[\d+] - \[ResponseEnterStage]\n^(?P<json>.+)$', re.MULTILINE)
LOG_SAVE_RE = re.compile(r'^.C. save binary success : (?P<path>.*)$', re.MULTILINE)
CURRENT_MAJOR = Version('1.6')
TEST_PATH = pathlib.Path(r'c:\users\k\p\mechaparabellum\tests\mecha.txt')
LOG_DIRECTORY = pathlib.Path(r'C:\Program Files (x86)\steam\steamapps\common\Mechabellum\ProjectDatas\Log\\')
# [Info][00:57:48 2025/07/30 +03:00] recv message [-1192] - [PushAddFpHistory]^M
# [{ "record": { "time": 1753826266, "eloPoint": -13, "mapId": 2021, "season": 4, "lobby": { "players": [ { "userid": "281474976710805718", "riskInfo": { "name": "JabaMaya", "faceUrl": "https://avatars.steamstatic.com/6a1f82166bffee647a9764f3f94cd6b26064b0d6_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } }, "index": 1 }, { "userid": "281474976710764850", "riskInfo": { "name": "Μ.Ξ.Ğ.Λ.Τ.Ř.Ø.Ņ.", "faceUrl": "https://avatars.steamstatic.com/f31c25ab959fc993b93f92bd2abcb80f4e482c82_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } } }, { "userid": "281474976711266755", "riskInfo": { "name": "Kalmere", "faceUrl": "https://avatars.steamstatic.com/fdd8590c4e2fb20011a0e762f3868729bffa8be2_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } }, "index": 2 } ], "win": -1, "index": 3 } } }]
GAME_RESULT_RE = re.compile(r'^\[Info]\[.*] recv message \[-?\d+] - \[PushAddFpHistory]\n^(?P<json>.+)$', re.MULTILINE)
SAVE_GAME_NAME_RE = re.compile('^(?P<version>\d+)_(?P<match_id>.+)_\[.*]VS\[.*]\.grbr')
COMBAT_RECORD_RE = re.compile(
    r'^\[Info]\[\d\d:\d\d:\d\d \d{4}/\d\d/\d\d \+\d\d:\d\d] recv message \[\d+] - \[ResponseFPDetail]\n^(?P<json>.+)$',
    re.MULTILINE,
)


# Combat record!
"""[Info][13:07:59 2025/07/31 +03:00] recv message [0] - [ResponseFPDetail]
[{json..}]
"""
# Game Over
"""[C] recv message [-30] - [PushGameOver]"""
# Round damage:
'[C] [5] team 0, reduce score 3496, current : -46 / 6600^M'

# MRR update:
"""[Info][13:40:44 2025/07/31 +03:00] recv message [-147] - [PushEloChange]^M
[{ "eloTimes2v2": 430, "eloScore2v2": 1157 }]"""

logger = logging.getLogger(__name__)

DATA_DIR = pathlib.Path(platformdirs.user_data_dir(APP_NAME, AUTHOR, ensure_exists=True))


class Result(enum.IntEnum):
    LOSS = -1
    UNKNOWN = 0
    WIN = 1

    def __rich__(self):
        if self.value == Result.LOSS:
            return '[red]Loss[/red]'
        elif self.value == Result.WIN:
            return '[green]Win[/green]'
        else:
            return 'n/a'


class Rank(enum.IntEnum):
    WINNER = 1
    RUNNER_UP = 2
    THIRD = 3
    FOURTH = 4

    def __rich__(self):
        return self.name.title()


class CLI:
    def __init__(self):
        self.console = Console()

    def _test(self):
        log_files = LOG_DIRECTORY.rglob('?Auto*.txt')
        for log_file in log_files:
            text = log_file.read_text()
            for result_match, save_match in zip(GAME_RESULT_RE.finditer(text), LOG_SAVE_RE.finditer(text)):
                path = pathlib.Path(save_match.group('path'))

                match_data = json.loads(result_match.group('json'))
                results = match_data[0]['record']
                mrr_change = results.get('eloPoint', 0)
                try:
                    outcome = Result(results['lobby']['win'])
                except KeyError:
                    outcome = Result(math.copysign(1, mrr_change) if mrr_change else 0)
                if match := SAVE_GAME_NAME_RE.match(path.name):
                    match_id = match.group('match_id')
                self.console.print(match_id, outcome.name, mrr_change, path.name)

    @staticmethod
    def _get_player_data(fight):
        for k in 'match', 'lobby', 'chaosFaction':
            try:
                return fight[k]
            except KeyError:
                continue
        raise KeyError(k)

    def _parse_logs(self):
        results = {}
        log_files = LOG_DIRECTORY.rglob('?Auto*.txt')
        for log_file in log_files:
            logger.debug(str(log_file.stem))
            text = log_file.read_text()
            for m in COMBAT_RECORD_RE.finditer(text):
                data = json.loads(m.group('json'))
                for fight in data[0]['records']:
                    try:
                        points = fight.get('point', 0)
                        map_id = fight['mapId']
                        season = fight['season']
                        mrr_change = fight.get('eloPoint', 0)
                        player_data = self._get_player_data(fight)
                        try:
                            seat = player_data.get('index', 0)
                        except KeyError:
                            seat = -1
                        try:
                            outcome = Result(player_data['win'])
                        except KeyError:
                            try:
                                outcome = Rank(player_data['rank'])
                            except KeyError:
                                outcome = Result(math.copysign(1, mrr_change) if mrr_change else 0)
                        ts = fight['time']
                        players = {
                            pl.get('index', 0): {'id_': pl['userid'], 'name': pl['riskInfo']['name']}
                            for pl in player_data['players']
                        }
                        # self.console.print(datetime.datetime.fromtimestamp(ts).isoformat(), outcome.name, seat, players)
                        results[ts] = {
                            'season': season,
                            'map_id': map_id,
                            'outcome': outcome,
                            'seat': seat,
                            'players': players,
                            'combat_power': points,
                            'mrr_change': mrr_change,
                        }
                    except KeyError:
                        self.console.print(fight)
        return results

    def parse(self):
        results = self._parse_logs()
        table = rich.table.Table()
        table.add_column('Season')
        table.add_column('Timestamp')
        table.add_column('Result')
        table.add_column('CP')
        table.add_column('MRR')
        table.add_column('P1')
        table.add_column('P2')
        table.add_column('P3')
        table.add_column('P4')
        for ts, result in sorted(results.items(), key=itemgetter(0)):
            result['timestamp'] = ts
            with (DATA_DIR / f'match_result_{ts}.json').open('w') as f:
                json.dump(result, f)

            def _get_playernames():
                players = result['players']
                if result['map_id'] > 3999:
                    colors = ['blue', 'red', 'green', 'yellow']
                elif len(players) > 2:
                    colors = ['blue', 'blue', 'red', 'red']
                else:
                    colors = ['blue', 'red', 'white', 'white']
                for idx in range(4):
                    try:
                        playername = players[idx]['name']
                    except KeyError:
                        if idx == result['seat']:
                            playername = '[bold]You[/bold]'
                        else:
                            playername = ''
                    name = f'[{colors[idx]}]{playername}[/{colors[idx]}]'
                    yield name

            table.add_row(
                str(result['season']),
                datetime.datetime.fromtimestamp(ts).isoformat(),
                result['outcome'],
                str(result['combat_power']),
                str(result['mrr_change']),
                *_get_playernames(),
            )
        self.console.print(f"That's {len(results)} results")
        self.console.print(table)

    def download(self):
        for i in range(NUMBER_OF_FORMATION_FILES):
            url = f'https://d3cyy8d63arovd.cloudfront.net/formation/0/base_{i:d}.json'
            res = requests.get(url)
            data = res.json()
            fn = DATA_DIR / f'recommended_{i:d}.json'
            with fn.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def analyze(self, rows=20):
        wins = Counter()
        picked = Counter()
        names = defaultdict(set)
        files = DATA_DIR.glob('recommended_*.json')
        for path in files:
            with path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                for formation in data:
                    try:
                        if Version(formation['version']) < CURRENT_MAJOR:
                            continue
                    except InvalidVersion:
                        continue
                        # print(datetime.datetime.fromtimestamp(int(formation['time'])))
                    units = (int(u['id']) for u in formation['units'])
                    key = tuple(Counter(units).items())
                    names[key].add(formation['name'])
                    wins[key] += int(formation['win_count'])
                    picked[key] += int(formation['select_count'])

        win_rates = {}
        popularities = {}
        total = picked.total()
        for form, win_count in wins.items():
            pick_count = picked[form]
            popularities[form] = pick_count / total
            try:
                win_rates[form] = win_count / pick_count
            except ZeroDivisionError:
                win_rates[form] = 0
        table = rich.table.Table(title='Best starting line-ups')
        table.add_column('Rank', justify='center')
        table.add_column('Win rate', justify='center')
        table.add_column('Popularity', justify='center')
        table.add_column()
        table.add_column()
        table.add_column()
        best_starting_units = Counter()
        rank = 1
        for form, winrate in sorted(win_rates.items(), key=itemgetter(1), reverse=True):
            if (popularity := popularities[form]) < 0.01:
                continue

            def _inner():
                yield f'#{rank:d}'
                yield f'{winrate:.1%}'
                yield f'{popularity:.1%}'
                for unit, n in sorted(form, key=itemgetter(1), reverse=True):
                    best_starting_units[unit] += win_count
                    yield (f'{str(n)} * {Unit(unit)}')

            table.add_row(*_inner())
            rank += 1
            if rank > rows:
                break
        self.console.print(table)

        table = rich.table.Table(title='Best starting units')
        table.add_column('Rank', justify='center')
        table.add_column('Wins', justify='center')
        table.add_column()
        for i, (unit, n) in enumerate(best_starting_units.most_common(rows), 1):
            table.add_row(str(i), str(n), str(Unit(unit)))

        self.console.print(table)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CLI)
