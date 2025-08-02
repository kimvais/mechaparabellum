import dataclasses
import enum

from mechaparabellum.actions import Action
from mechaparabellum.units import Specialist, \
    Unit

@dataclasses.dataclass
class Player:
    id_: int
    name: str
    seat: int


@dataclasses.dataclass
class PlayerRound:
    number: int
    player: Player
    supply: int
    health: int
    specialists: list[Specialist]
    unlocked_units: list[Unit]
    actions: list[Action]
    #pre_round_result: Result
    # units: list[DeployedUnit]


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
