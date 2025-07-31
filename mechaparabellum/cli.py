import enum
import logging
import math
import pathlib
import re
import json
from collections import Counter, defaultdict
from operator import itemgetter
from packaging.version import InvalidVersion, Version

from rich.console import Console
import rich.table
import fire
import requests

from mechaparabellum.utils import get_newest
from mechaparabellum.units import Unit

NUMBER_OF_FORMATION_FILES = 10

GAME_START_RE = re.compile(r'^\[C] recv message \[\d+] - \[ResponseEnterStage]\n^(?P<json>.+)$', re.MULTILINE)
LOG_SAVE_RE = re.compile(r'^.C. save binary success : (?P<path>.*)$', re.MULTILINE)
CURRENT_MAJOR = Version('1.6')
DATA_DIR = pathlib.Path(__file__).parent / 'data'
TEST_PATH = pathlib.Path(r'c:\users\k\p\mechaparabellum\tests\mecha.txt')
LOG_DIRECTORY = pathlib.Path(r'C:\Program Files (x86)\steam\steamapps\common\Mechabellum\ProjectDatas\Log\\')
# [Info][00:57:48 2025/07/30 +03:00] recv message [-1192] - [PushAddFpHistory]^M
# [{ "record": { "time": 1753826266, "eloPoint": -13, "mapId": 2021, "season": 4, "lobby": { "players": [ { "userid": "281474976710805718", "riskInfo": { "name": "JabaMaya", "faceUrl": "https://avatars.steamstatic.com/6a1f82166bffee647a9764f3f94cd6b26064b0d6_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } }, "index": 1 }, { "userid": "281474976710764850", "riskInfo": { "name": "Μ.Ξ.Ğ.Λ.Τ.Ř.Ø.Ņ.", "faceUrl": "https://avatars.steamstatic.com/f31c25ab959fc993b93f92bd2abcb80f4e482c82_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } } }, { "userid": "281474976711266755", "riskInfo": { "name": "Kalmere", "faceUrl": "https://avatars.steamstatic.com/fdd8590c4e2fb20011a0e762f3868729bffa8be2_full.jpg", "blockName": { "1": false, "2": false, "3": false }, "blockFace": { "1": false, "2": false, "3": false } }, "index": 2 } ], "win": -1, "index": 3 } } }]
GAME_RESULT_RE = re.compile(r'^\[Info]\[.*] recv message \[-?\d+] - \[PushAddFpHistory]\n^(?P<json>.+)$', re.MULTILINE)

logger = logging.getLogger(__name__)


class Result(enum.IntEnum):
    LOSS = -1
    UNKNOWN = 0
    WIN = 1

class CLI:
    def __init__(self):
        self.console = Console()

    def test(self):
        log_files = LOG_DIRECTORY.rglob('?Auto*.txt')
        for log_file in log_files:
            text = log_file.read_text()
            for result_match, save_match in zip(GAME_RESULT_RE.finditer(text), LOG_SAVE_RE.finditer(text)):
                path = save_match.group('path')
                match_data = json.loads(result_match.group('json'))
                results = match_data[0]['record']
                mrr_change = results.get('eloPoint', 0)
                try:
                    outcome = Result(results['lobby']['win'])
                except KeyError:
                    outcome = Result(math.copysign(1, mrr_change) if mrr_change else 0)
                self.console.print(outcome.name, mrr_change, path)

    def test2(self):
        log_files = LOG_DIRECTORY.rglob('?Auto*.txt')
        for log_file in log_files:
            logger.debug(str(log_file.stem))
            text = log_file.read_text()
            print(text.count('save binary success'))
            for m in LOG_SAVE_RE.finditer(text):
                self.console.print(m.group('path'))

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
