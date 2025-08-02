import abc
import dataclasses

from mechaparabellum.units import CommanderSkill, Contraption, Item, Reinforcement, Tower, TowerTech, Unit, UnitTech
from mechaparabellum.utils import get_unit, to_str

actions = {}


def action_dataclass(cls):
    cls.action_name = f'PAD_{cls.__name__}'
    actions[cls.action_name] = cls
    return dataclasses.dataclass(cls)


class Action(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def parse(self, elem):
        raise NotImplementedError

    def __rich__(self):
        return self.__str__

    def __str__(self):
        return self.__class__.__name__


class _UnitAction(Action):
    unit: Unit

    @classmethod
    def parse(cls, elem):
        yield cls(unit=get_unit(elem))


@action_dataclass
class ChooseAdvanceTeam(Action):
    uid: int
    index: int

    @classmethod
    def parse(cls, elem):
        uid = elem.find('ID').text
        index = elem.find('Index').text
        yield cls(uid, index)

    def __str__(self):
        return f'Choose starting setup: #{self.index}: {self.uid}'


@action_dataclass
class UpgradeTechnology(Action):
    unit: Unit
    tech = UnitTech

    @classmethod
    def parse(cls, elem):
        unit = get_unit(elem)
        tech, teched_unit = UnitTech.parse(elem.find('TechID').text, unit)
        assert teched_unit in {Unit.DEPRECATED, unit}, (
            tech,
            unit,
            to_str(elem),
        )
        yield cls(unit, tech)

    def __str__(self):
        return f'Upgrade technology: {self.unit} ({self.unit.value}) - {self.tech} ({self.tech.value})'


@action_dataclass
class ActiveEnergyTowerSkill(Action):
    skill: TowerTech

    @classmethod
    def parse(cls, elem):
        skill = TowerTech(int(elem.find('SkillID').text))
        yield cls(skill)

    def __str__(self):
        return f'Active energy tower skill: {self.skill}'


@action_dataclass
class BuyUnit(_UnitAction):
    def __str__(self):
        return f'Buy unit: {self.unit}'


@action_dataclass
class UnlockUnit(_UnitAction):
    def __str__(self):
        return f'Unlock unit: {self.unit}'


@action_dataclass
class UpgradeUnit(Action):
    unit: Unit
    index: int

    @classmethod
    def parse(cls, elem):
        index = int(elem.find('UIDX').text)
        yield cls(get_unit(elem), index)

    def __str__(self):
        return f'Upgrade unit: {self.unit} ({self.unit.value}) - {self.index}'


@action_dataclass
class Undo(Action):
    @classmethod
    def parse(cls, elem):
        yield cls()


@action_dataclass
class FinishDeploy(Action):
    @classmethod
    def parse(cls, elem):
        yield (cls)

    def __str__(self):
        return f'Finish deploy'


@action_dataclass
class ReleaseCommanderSkill(Action):
    skill: CommanderSkill
    index: int

    @classmethod
    def parse(cls, elem):
        skill = CommanderSkill(int(elem.find('ID').text))
        index = int(elem.find('SkillIndex').text)
        yield cls(skill, index)

    def __str__(self):
        return f'Release commander skill: {self.skill}'


@action_dataclass
class PAD_MoveUnit(Action):
    unit: Unit
    index: int
    x: int
    y: int

    @classmethod
    def parse(cls, elem):
        moves = elem.xpath('moveUnitDatas/MoveUnitData')
        for data in moves:
            x = data.find('position').find('x').text
            y = data.find('position').find('y').text
            unit = Unit(int(data.find('unitID').text))
            index = data.find('unitIndex').text
            yield cls(unit, index, x, y)

    def __str__(self):
        return f'Move unit: {self.unit} #{self.index} x: {self.x} y: {self.y}'


@action_dataclass
class ChooseReinforcement(Action):
    item: Reinforcement
    index: int

    @classmethod
    def parse(cls, elem):
        item = Reinforcement(int(elem.find('ID').text))
        index = int(elem.find('Index').text)
        yield cls(item, index)

    def __str__(self):
        return f'Choose reinforcement: {self.item} (@ {self.index})'


@action_dataclass
class UseEquipment(Action):
    item: Item
    index: int

    @classmethod
    def parse(cls, elem):
        item = Item(int(elem.find('EquipmentID').text))
        index = int(elem.find('UnitIndex').text)
        yield cls(item, index)

    def __str__(self):
        return f'Use equipment: {self.item} (On unit @{self.index})'


@action_dataclass
class ActivateBlueprint(Action):
    id_: int

    @classmethod
    def parse(cls, elem):
        id_ = int(elem.find('ID').text)
        yield cls(id_)

    def __str__(self):
        return f'Activate blueprint: {self.id_}'


@action_dataclass
class GiveUp(Action):
    @classmethod
    def parse(cls, elem):
        yield cls()

    def __str__(self):
        return 'Surrender'


@action_dataclass
class ReleaseContraption(Action):
    contraption: Contraption

    @classmethod
    def parse(cls, elem):
        yield cls(Contraption(int(elem.find('ContraptionID').text)))

    def __str__(self):
        return f'Release contraption: {self.contraption}'


@action_dataclass
class StrengthenTower(Action):
    tower: Tower

    @classmethod
    def parse(cls, elem):
        _idx = elem.find('Index').text
        yield cls(Tower(int(_idx)))

    def __str__(self):
        return f'Strengthen tower: {self.tower}'


@action_dataclass
class CancelReleaseCommanderSkill(Action):
    skill: CommanderSkill

    @classmethod
    def parse(cls, elem):
        _id = int(elem.find('ID').text)
        yield cls(CommanderSkill(_id))

    def __str__(self):
        return f'Cancel release commander skill: {self.skill}'


@action_dataclass
class TestCommand(Action):
    @classmethod
    def parse(cls, elem):
        yield cls()

    def __str__(self):
        return '[red]TESTING GROUNDS ARE NOT SUPPORTED[/red]'
