import pathlib
import re
import json
from collections import Counter, \
    defaultdict
from operator import itemgetter
from packaging.version import InvalidVersion, \
    Version

from rich.console import Console
import rich.table
import fire
import requests

from mechaparabellum.utils import get_newest
from mechaparabellum.units import Unit

NUMBER_OF_FORMATION_FILES = 10

GAME_START_RE = re.compile(r'^\[C] recv message \[\d+] - \[ResponseEnterStage]\n^(?P<json>.+)$', re.MULTILINE)
CURRENT_MAJOR = Version('1.6')
DATA_DIR = pathlib.Path(__file__).parent / 'data'
TEST_PATH = pathlib.Path(r'c:\users\k\p\mechaparabellum\tests\mecha.txt')
LOG_DIRECTORY = pathlib.Path(r"C:\Program Files (x86)\steam\steamapps\common\Mechabellum\ProjectDatas\Log\\")


class CLI:
    def __init__(self):
        self.console = Console()

    def test(self):
        log_files = LOG_DIRECTORY.rglob('?Auto*.txt')
        newest = get_newest(log_files)
        print(newest.lstat())
        log = newest.read_text()
        for re_match in GAME_START_RE.finditer(log):
            print(re_match)
            match_data = json.loads(re_match.group('json'))
        self.console.print(match_data)

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
                for unit, n in sorted(form, key=itemgetter(1), reverse = True):
                    best_starting_units[unit] += win_count
                    yield(f'{str(n)} * {Unit(unit)}')
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
    fire.Fire(CLI)

