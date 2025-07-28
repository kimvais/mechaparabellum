import pathlib
import re
import json
from collections import Counter, \
    defaultdict
from operator import itemgetter
from packaging.version import InvalidVersion, \
    Version

from rich.console import Console
import fire
import requests

from mechaparabellum.utils import get_newest
from mechaparabellum.units import Unit

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
        for i in range(9):
            url = f'https://d3cyy8d63arovd.cloudfront.net/formation/0/base_{i:d}.json'
            res = requests.get(url)
            data = res.json()
            fn = DATA_DIR / f'recommended_{i:d}.json'
            with fn.open('w', encoding='utf-8') as f:
                json.dump(res.json(), f, ensure_ascii=False, indent=4)
            # self.console.print(data)

    def analyze(self):
        wins = Counter()
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
                    n = formation['win_count']
                    key = tuple(Counter(units).items())
                    names[key].add(formation['name'])
                    wins[key] += int(n)
        for form, win_count in wins.most_common(10):
            players = names[form]
            # self.console.print(form, players)


        self.console.print(wins.most_common(10))
        for k, v in names.items():
            if 'NTAGT' in v and (2, 2) in k:
                print(k, v)
        print(names[((2, 2), (28, 3), (12, 2))])
        alls = set()
        for key in wins.keys():
            alls |= set(key)
        unit_numbers = defaultdict(set)
        for id_, count in sorted(alls, key=itemgetter(1), reverse=True):
            unit_numbers[id_].add(count)
        self.console.print(unit_numbers)
        self.console.print(sorted(unit_numbers.keys()))


if __name__ == '__main__':
    fire.Fire(CLI)

