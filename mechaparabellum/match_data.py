import dataclasses
import enum

from mechaparabellum.actions import Action
from mechaparabellum.units import Specialist, \
    Unit

"""
Coordinate system:

- Origin is at the middle of the no-man's land.
- All coordinates are for the center point.
- Flanks are 60m wide, ranging in x from -360 to -300 and 300 to 360 
- Main battlefield is 600m wide, ranging in x from -300 to 300
- The battlefield is 620m tall, ranging from -10 to -320 (player's side, top top bottom)
- There is a 20m wide tall no-mans land in the middle, ranging from 10 to -10
- Flanks range in y from 310 to 10 (top to bottom)

+-------------------------+
|(-300, -10)    (300, -10)|  
|                         |
|                         |
|(-300, -310)  (300, -310)|
+-------------------------+
"""

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
