import logging
import sys

import fire
from lxml import etree
from xml.etree import ElementTree as ET
import pathlib
import tempfile

from mechaparabellum.units import CommanderSkill, \
    Contraption, \
    Item, \
    Reinforcement, \
    Tower, \
    TowerTech, \
    Unit, \
    UnitTech


DIR = pathlib.Path('C:/Program Files (x86)/Steam/steamapps/common/Mechabellum/ProjectDatas/Replay')
OUT_DIR = pathlib.Path('c:/Users/k/p/mechaparabellum/replays')
STATIC = 0x151
DATE_END = 0x166
XML_START = 0x18a
START_TAG = b'<BattleRecord xmlns'
END_TAG = b'</BattleRecord>'

PLAYER = 'Kimvais'

def load(path):
    data = path.read_bytes()
    xml_start = data.find(START_TAG)
    xml_end = data.find(END_TAG)
    xml = data[xml_start:xml_end+len(END_TAG)].decode('utf-8')
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

class CLI:
    @staticmethod
    def parse(path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        root = load(path)
        player_record = find_correct_pr(root.find('playerRecords'))
        for round in player_record.find('playerRoundRecords'):
            round_no = round.find("round").text
            print(f'\n\n --- Round: {round_no}')
            unlocked_units = round.xpath('playerData/shop/unlockedUnits/int')
            actions = round.xpath('actionRecords/MatchActionData')
            for unit in unlocked_units:
                print(f' Available: {Unit(int(unit.text))}')
            for action in actions:
                act_name = action.attrib.values()[0]
                try:
                    match act_name:
                        case 'PAD_ChooseAdvanceTeam':
                            uid = action.find('ID').text
                            idx = action.find('Index').text
                            print(f'Choose starting setup: #{idx}: {uid}')
                        case 'PAD_UpgradeTechnology':
                            unit = get_unit(action)
                            tech, teched_unit  = UnitTech.parse(action.find('TechID').text)
                            assert unit == teched_unit, (tech, unit, to_str(action))
                            print(f'Upgrade technology: {unit} - {tech}')
                        case 'PAD_ActiveEnergyTowerSkill':
                            skill = TowerTech(int(action.find('SkillID').text))
                            print(f'Active energy tower skill: {skill}')
                        case 'PAD_BuyUnit':
                            uid = get_unit(action)
                            print(f'Buy unit: {uid}')
                        case 'PAD_UnlockUnit':
                            uid = get_unit(action)
                            print(f'Unlock unit: {uid}')
                        case 'PAD_UpgradeUnit':
                            uid = get_unit(action)
                            idx = action.find('UIDX').text
                            print(f'Upgrade unit: {uid} #{idx}')
                        case 'PAD_FinishDeploy':
                            print('Finish deploy')
                        case 'PAD_Undo':
                            print('Undo')
                        case 'PAD_ReleaseCommanderSkill':
                            skill_id = int(action.find('ID').text)
                            skill = CommanderSkill(skill_id)
                            index = int(action.find('SkillIndex').text)
                            print(f'Release commander skill: {skill}')
                        case 'PAD_MoveUnit':
                            moves = action.xpath('moveUnitDatas/MoveUnitData')
                            for data in moves:
                                x = data.find('position').find('x').text
                                y = data.find('position').find('y').text
                                uid = Unit(int(data.find('unitID').text))
                                index = data.find('unitIndex').text
                                print(f'Move unit: {uid} #{index} x: {x} y: {y}')
                        case 'PAD_ChooseReinforceItem':
                            idx = action.find('Index').text
                            uid = action.find('ID').text
                            item = Reinforcement.parse(uid)
                            print(f'Choose reinforcement: {item} ({idx})')
                        case 'PAD_UseEquipment':
                            uid = action.find('EquipmentID').text
                            item = Item(int(uid))
                            idx = action.find('UnitIndex').text
                            print(f'Use equipment: {item} on unit #{idx}')
                        case 'PAD_ActiveBlueprint':
                            uid = action.find('ID').text
                            print(f'Activate spell: {uid}')
                        case 'PAD_GiveUp':
                            print('Surrender')
                        case 'PAD_ReleaseContraption':
                            uid = int(action.find('ContraptionID').text)
                            item = Contraption(int(uid))
                            print(f'Release contraption: {item}')
                        case 'PAD_StrengthenTower':
                            tower_idx = action.find('Index').text
                            tower = Tower(int(tower_idx))
                            print(f'Strengthen tower: {tower}')
                        case 'PAD_CancelReleaseCommanderSkill':
                            skill_id = int(action.find('ID').text)
                            skill = CommanderSkill(skill_id)
                            print(f'Cancel release commander skill {skill}')
                        case _:
                            print(to_str(action))
                            raise Exception(f'Unknown action: {action}')
                except AttributeError as e:
                    logging.exception(e)
                    print(to_str(action))
                except ValueError:
                    print(to_str(action))
                    print(f'{path.stem} on round # {round_no}')
                    sys.exit(1)

    def parse_all(self):
        for path in DIR.glob('*.grbr'):
            print(f'Parsing {path.name}')
            self.parse(path)



if __name__ == '__main__':
    fire.Fire(CLI)
