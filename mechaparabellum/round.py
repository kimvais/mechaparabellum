import dataclasses

from mechaparabellum.actions import Action
from mechaparabellum.cli import Result
from mechaparabellum.units import Specialist, \
    Unit


@dataclasses.dataclass
class PlayerRound:
    number: int
    player: str
    supply: int
    health: int
    specialists: list[Specialist]
    unlocked_units: list[Unit]
    actions: list[Action]
    #pre_round_result: Result
    # units: list[DeployedUnit]

