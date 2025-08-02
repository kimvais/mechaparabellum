import dataclasses
import enum
import logging
import sys

import fire
from lxml import etree
import pathlib
import tempfile

from rich.console import Console

from mechaparabellum.actions import ChooseAdvanceTeam, \
    actions
from mechaparabellum.round import PlayerRound
from mechaparabellum.units import (
    CommanderSkill,
    Contraption,
    Item,
    Reinforcement,
    Specialist,
    Tower,
    TowerTech,
    Unit,
    UnitTech,
)
from mechaparabellum.utils import modification_time, to_str


DIR = pathlib.Path('C:/Program Files (x86)/Steam/steamapps/common/Mechabellum/ProjectDatas/Replay')
OUT_DIR = pathlib.Path('c:/Users/k/p/mechaparabellum/replays')
STATIC = 0x151
DATE_END = 0x166
XML_START = 0x18A
START_TAG = b'<BattleRecord xmlns'
END_TAG = b'</BattleRecord>'

PLAYER = 'Kimvais'

logger = logging.getLogger(__name__)


def load(path):
    data = path.read_bytes()
    xml_start = data.find(START_TAG)
    xml_end = data.find(END_TAG)
    xml = data[xml_start : xml_end + len(END_TAG)].decode('utf-8')
    _, fn = tempfile.mkstemp('.xml', text=True)
    xml_path = pathlib.Path(fn)
    xml_path.write_text(xml)
    tree = etree.parse(xml_path, parser=etree.XMLParser(recover=True))
    # xml_path.unlink()
    return tree.getroot()


def find_correct_pr(prs):
    for pr in prs:
        name = pr.find('name')
        if name is None:
            continue
        print(name.text)
        if name.text == PLAYER:
            return pr


def get_unit(action):
    uid = action.find('UID').text
    return Unit(int(uid))


class MatchMode(enum.Enum):
    _1V1 = 'VS_1_1'
    _2V2 = 'VS_2_2'
    BRAWL = 'VS_4_Scuffle'

    def __str__(self):
        return self.name.lstrip('_'.title())

    __rich__ = __str__


@dataclasses.dataclass
class BattleInfo:
    id_: str
    game_mode: str
    match_mode: MatchMode


class CLI:
    def __init__(self, debug=False):
        self.debug = debug
        self.console = Console()
        self.buffer = []
        self._debug_data = {}

    def output(self, msg):
        self.buffer.append(msg)
        self.console.print(msg)

    def parse(self, path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        root = load(path)

        # Root parsing
        version = root.find('Version').text
        seat = int(root.find('Seat').text)

        # Battle info parsing
        battle_info = root.find('BattleInfo')
        battle = BattleInfo(
            id_=battle_info.find('BattleID').text,
            game_mode=battle_info.find('GameMode').text,
            match_mode=MatchMode(battle_info.find('MatchMode').text),
        )
        self.output(dataclasses.asdict(battle))
        # Player record parsing
        player_records = root.find('playerRecords')
        self.output(f'Battle ID: {battle.id_} on {version}, seat {seat}')
        for index, pr in enumerate(player_records[:4]):  # This skips bots in brawl
            round_list = pr.find('playerRoundRecords').getchildren()
            if not round_list:
                logger.error(f'No rounds found!')
                continue
            name = pr.find('name').text
            try:
                specialist_id = int(round_list[-1].xpath('playerData/officers')[0].find('int').text)
            except AttributeError:
                specialist_id = -1
            try:
                specialist = Specialist(specialist_id)
            except ValueError:
                self.output(f'Unknown specialist for "{name}": {specialist_id}')
                sys.exit(1)

            self.output(f'Player #{index}: {name}: {specialist}')

        try:
            player_record = player_records.getchildren()[seat]
        except IndexError:
            self.output(f'Seat {seat} out of range, player is a spectator!')
            return
        else:
            player_name = player_record.find('name').text
            assert player_name == PLAYER
        # reinforceItems
        # Version
        # Seat
        # BattleInfo:
        # StartTime 0
        # SystemSeed ###
        # BattleID ###-###
        # PrepareTime 30
        # DeployTime 100
        # FightTime 120 / 200 (1v1 / 2v2)
        # MapID 2011
        # MaxRound 40
        # BlueprintIncreaseSupply 0
        # EnableAdvanceTeam "true" (Ganks?)
        # EnableReinforcement "true" (Drops?)
        # GameMode "Normal" / "Competition" (Tournament?)
        # MatchMode "VS_2_2" / "VS_1_1" / "VS_4_Scuffle"
        # ScoreMode "ReduceScore"
        # HostID 0
        # CloseUnitReinforce "false"
        # SurviveModeDifficulty "VeryEasy"
        match_datas = root.xpath('matchDatas/MatchSnapshotData')  # a list, per round
        # poolOPs/ValueTupleOfInt32Int32 - drop choices Item1 0, Item2 ID
        # lastFightResult/Reports: a list, per player
        # FightReport:
        # Contraptions/ContraptionData
        # unitData/NewUnitData[]: id, Index, RoundCount, Durability (survival?), Exp, Level
        # Score
        # DeadScore
        # DestroydCrystalCount
        # AliveMechCount
        # /data
        # - reactorCore, MacReactorCore, maxRoundSypply, firstRoundSupply, roundSupplyIncreaseValue, team, isLeader
        # - style (just skin data), unitDatas[]/unitData:
        #   - id, techs[]/tech[data]
        round_records = player_record.find('playerRoundRecords')
        for round in round_records:
            player_round = self._parse_round(path, round)
            if self.debug:
                self.output(player_round)

    def _parse_int(self, elem):
        return int(elem[0].text)

    def _parse_round(self, path, round):
        round_no = int(round.find('round').text)
        if round_no == 1:
            self._debug_data[self._debug_data['team']] = []
        unlocked_units = round.xpath('playerData/shop/unlockedUnits/int')
        hp = round.xpath('playerData/reactorCore')
        supply = round.xpath('playerData/supply')
        units = round.xpath('playerData/units')
        # ... NewUnitData : id, Index, RoundCount, Exp, Level, Position/x, Position/y, EquipmentID, IsRotate, SellSupply
        specialist = round.xpath('playerData/officers')
        unit_count = round.xpath('playerData/unitIndex')
        # playerData:
        # preRoundFightResult "Lose" / "Win"
        # commanderSkills
        # activeTechnologies
        # equipments
        # shop/BuyCount, shop/MaxUnlockCount, shop/UnlockCount
        # contraptions
        # blueprints
        # energyTowerSkills
        # towerStrengthLevels 0,1
        # isSpecialSupply (bool)
        for unit in unlocked_units:
            unit = Unit(int(unit.text))
            if round_no == 1:
                self._debug_data[self._debug_data['team']].append(unit)
        actions = list(self._parse_actions(round.xpath('actionRecords/MatchActionData')))
        if isinstance(actions[0], ChooseAdvanceTeam):
            self._debug_data['team'] = actions[0].uid
        return PlayerRound(
            number=round_no,
            player=PLAYER,
            supply=self._parse_int(supply),
            health=self._parse_int(hp),
            specialists=[Specialist(int(elem.find('int').text)) for elem in specialist if elem.text is not None],
            unlocked_units=[
                Unit(int(elem.text))
                            for elem
                            in unlocked_units
            ],
            actions=actions,
        )


    def _parse_actions(self, actions):
        for action in actions:
            try:
                yield from self._parse_action(action)
            except AttributeError as e:
                logging.exception(e)
                self.output(to_str(action))
            except ValueError as e:
                logging.exception(e)
                self.output(to_str(action))
                sys.exit(1)

    def _parse_action(self, xml_action_elem):
        act_name = xml_action_elem.attrib.values()[0]
        try:
            cls = actions[act_name]
        except KeyError:
            self.output(to_str(xml_action_elem))
            raise Exception(f'Unknown action: {xml_action_elem}')

        yield from cls.parse(xml_action_elem)

    def parse_all(self):
        for n, path in enumerate(sorted(DIR.glob('*.grbr'), key=modification_time, reverse=True), 1):
            self.output(f'Parsing #{n} {path.name}')
            self.parse(path)
        self.output(self._debug_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CLI)
