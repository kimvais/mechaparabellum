import dataclasses
import enum
import logging
import sys

import fire
from lxml import etree
from xml.etree import ElementTree as ET
import pathlib
import tempfile

from rich.console import Console

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
from mechaparabellum.utils import modification_time


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


def to_str(elem):
    return ET.tostring(elem).decode('utf-8')


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
    def __init__(self):
        self.console = Console()

    def parse(self, path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        root = load(path)

        # Root parsing
        version = root.find('Version').text
        seat = int(root.find('Seat').text)

        # Battle info parsing
        battle_info= root.find('BattleInfo')
        battle = BattleInfo(
        id_ = battle_info.find('BattleID').text,
        game_mode = battle_info.find('GameMode').text,
        match_mode = MatchMode(battle_info.find('MatchMode').text),
        )
        self.console.print(dataclasses.asdict(battle))
        # Player record parsing
        player_records = root.find('playerRecords')
        self.console.print(f'Battle ID: {battle.id_} on {version}, seat {seat}')
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
                self.console.print(f'Unknown specialist for "{name}": {specialist_id}')
                sys.exit(1)

            self.console.print(f'Player #{index}: {name}: {specialist}')

        player_record = player_records.getchildren()[seat]
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
        if player_record is None:
            return
        # /data
        # - reactorCore, MacReactorCore, maxRoundSypply, firstRoundSupply, roundSupplyIncreaseValue, team, isLeader
        # - style (just skin data), unitDatas[]/unitData:
        #   - id, techs[]/tech[data]
        round_records = player_record.find('playerRoundRecords')
        for round in round_records:
            round_no = round.find('round').text
            self.console.print(f'\n\n --- Round: {round_no}')
            unlocked_units = round.xpath('playerData/shop/unlockedUnits/int')
            hp = round.xpath('playerData/reactorCore')
            supply = round.xpath('playerData/supply')
            units = round.xpath('playerData/units')
            # ... NewUnitData : id, Index, RoundCount, Exp, Level, Position/x, Position/y, EquipmentID, IsRotate, SellSupply
            specialist = round.xpath('playerData/officers[0]')
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

            actions = round.xpath('actionRecords/MatchActionData')
            for unit in unlocked_units:
                self.console.print(f' Available: {Unit(int(unit.text))}')
            for action in actions:
                act_name = action.attrib.values()[0]
                try:
                    match act_name:
                        case 'PAD_ChooseAdvanceTeam':
                            uid = action.find('ID').text
                            idx = action.find('Index').text
                            self.console.print(f'Choose starting setup: #{idx}: {uid}')
                        case 'PAD_UpgradeTechnology':
                            unit = get_unit(action)
                            tech, teched_unit = UnitTech.parse(action.find('TechID').text, unit)
                            assert teched_unit in {Unit.DEPRECATED, unit}, (
                                tech,
                                unit,
                                to_str(action),
                            )
                            self.console.print(f'Upgrade technology: {unit} {unit.value} - {tech} {tech.value}')
                        case 'PAD_ActiveEnergyTowerSkill':
                            skill = TowerTech(int(action.find('SkillID').text))
                            self.console.print(f'Active energy tower skill: {skill}')
                        case 'PAD_BuyUnit':
                            uid = get_unit(action)
                            self.console.print(f'Buy unit: {uid}')
                        case 'PAD_UnlockUnit':
                            uid = get_unit(action)
                            self.console.print(f'Unlock unit: {uid}')
                        case 'PAD_UpgradeUnit':
                            uid = get_unit(action)
                            idx = action.find('UIDX').text
                            self.console.print(f'Upgrade unit: {uid} #{idx}')
                        case 'PAD_FinishDeploy':
                            self.console.print('Finish deploy')
                        case 'PAD_Undo':
                            self.console.print('Undo')
                        case 'PAD_ReleaseCommanderSkill':
                            skill_id = int(action.find('ID').text)
                            skill = CommanderSkill(skill_id)
                            index = int(action.find('SkillIndex').text)
                            self.console.print(f'Release commander skill: {skill}')
                        case 'PAD_MoveUnit':
                            moves = action.xpath('moveUnitDatas/MoveUnitData')
                            for data in moves:
                                x = data.find('position').find('x').text
                                y = data.find('position').find('y').text
                                uid = Unit(int(data.find('unitID').text))
                                index = data.find('unitIndex').text
                                self.console.print(f'Move unit: {uid} #{index} x: {x} y: {y}')
                        case 'PAD_ChooseReinforceItem':
                            idx = action.find('Index').text
                            uid = action.find('ID').text
                            item = Reinforcement.parse(uid)
                            self.console.print(f'Choose reinforcement: {item} ({idx})')
                        case 'PAD_UseEquipment':
                            uid = action.find('EquipmentID').text
                            item = Item(int(uid))
                            idx = action.find('UnitIndex').text
                            self.console.print(f'Use equipment: {item} on unit #{idx}')
                        case 'PAD_ActiveBlueprint':
                            uid = action.find('ID').text
                            self.console.print(f'Activate spell: {uid}')
                        case 'PAD_GiveUp':
                            self.console.print('Surrender')
                        case 'PAD_ReleaseContraption':
                            uid = int(action.find('ContraptionID').text)
                            item = Contraption(int(uid))
                            self.console.print(f'Release contraption: {item}')
                        case 'PAD_StrengthenTower':
                            tower_idx = action.find('Index').text
                            tower = Tower(int(tower_idx))
                            self.console.print(f'Strengthen tower: {tower}')
                        case 'PAD_CancelReleaseCommanderSkill':
                            skill_id = int(action.find('ID').text)
                            skill = CommanderSkill(skill_id)
                            self.console.print(f'Cancel release commander skill {skill}')
                        case 'PAD_TestCommand':
                            self.console.print('[red]TESTING GROUNDS ARE NOT SUPPORTED[/red]')
                        case _:
                            self.console.print(to_str(action))
                            raise Exception(f'Unknown action: {action}')
                except AttributeError as e:
                    logging.exception(e)
                    self.console.print(to_str(action))
                except ValueError as e:
                    logging.exception(e)
                    self.console.print(to_str(action))
                    self.console.print(f'{path.stem} on round # {round_no}')
                    sys.exit(1)

    def parse_all(self):
        for n, path in enumerate(sorted(DIR.glob('*.grbr'), key=modification_time, reverse=True), 1):
            self.console.print(f'Parsing #{n} {path.name}')
            self.parse(path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CLI)
