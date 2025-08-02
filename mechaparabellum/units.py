from __future__ import annotations
import dataclasses
import enum


"""
    18: {1},
    26: {1},
    19: {1},
    3: {1},
    14: {1},
    22: {1},
    11: {1},
    1: {1}

"""

CONFIRMED_UNIT_REINFORCEMENTS_FOR_1V1_AND_2V2 = {101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112}
CONFIRMED_UNIT_REINFORCEMENTS_FOR_BRAWL = {202, 205, 208}
CONFIRMED_UNIT_REINFORCEMENTS_FOR_SURVIVAL = {302, 303, 304, 305, 306, 307, 308, 309, 310}

CONFIRMED_UNIT_REINFORCEMENTS = (
    CONFIRMED_UNIT_REINFORCEMENTS_FOR_1V1_AND_2V2
    | CONFIRMED_UNIT_REINFORCEMENTS_FOR_BRAWL
    | CONFIRMED_UNIT_REINFORCEMENTS_FOR_SURVIVAL
)

DEDUCED_UNIT_REINFORCEMENTS = {201, 203, 204, 206, 207, 209, 210, 212}


class NamedEnum(enum.IntEnum):
    def __str__(self):
        return self.name.replace('_', ' ').title()


class Unit(NamedEnum):
    # Placeholder for units that get moved from mode to another:
    DEPRECATED = -1
    # The actual units, in ID order for reference.
    FORTRESS = 1
    MARKSMAN = 2
    VULCAN = 3
    MELTING_POINT = 4
    RHINO = 5
    WASP = 6
    MUSTANG = 7
    STEEL_BALL = 8
    FANG = 9
    CRAWLER = 10
    OVERLORD = 11
    STORMCALLER = 12
    SLEDGEHAMMER = 13
    HACKER = 14
    ARCLIGHT = 15
    PHOENIX = 16
    WAR_FACTORY = 17
    WRAITH = 18
    SCORPION = 19
    FIRE_BADGER = 20
    SABERTOOTH = 21
    TYPHOON = 22
    SANDWORM = 23
    TARANTULA = 24
    PHANTOM_RAY = 25
    FARSEER = 26
    RAIDEN = 27
    HOUND = 28
    ABYSS = 29
    VOID_EYE = 30
    DEATH_KNELL = 2001
    MOUNTAIN = 2002


class Item(NamedEnum):
    # Alphabetical order
    ABSORPTION_MODULE = 1309001  # 150
    AMPLIFYING_CORE = 13030007  # 150
    ANTI_INTERFERENCE_MODULE = 1308001
    BARRIER = 1307001
    DEPLOYMENT_MODULE = 13040001  # ???
    ENHANCEMENT_MODULE = 13030004
    HASTE_MODULE = 13030005
    HEAVY_ARMOR = 13030002
    IMPROVED_FIREPOWER_CONTROL_SYSTEM = 13030003  # ???
    LASER_SIGHTS = 13030001
    NANO_REPAIR_KIT = 13020001
    MUSTANG_PRODUCTION_LINE = 1306002
    PHOTON_COATING = 1305003
    PORTABLE_SHIELD = 13010001
    SMALL_AMPLIFYING_CORE = 13030009
    STEEL_BALL_PRODUCTION_LINE = 1306003
    SUPER_HEAVY_ARMOR = 13030006
    TANK_PRODUCTION_LINE = 1306001


class Reinforcement(NamedEnum):
    # Units = M[01].XRUU, where:
    #  - M is game mode, 1 for 1v1 and 2v2, 2 for Brawl and 3 for survival.
    #  - X is amount
    #  - R is rank
    #  - UU is unit ID
    #  - . is ???
    # 0000 in string format = spell
    # Unit modifiers = 3UU??
    # Items = 130+

    # Numerical order.
    _SKIP = 0
    # 1000* "always on" buffs (?)
    QUICK_COOLDOWN = 10001
    # 10002 ?
    SUPER_SUPPLY_ENHANCEMENT = 10003
    ADDITIONAL_DEPLOYMENT_SLOT = 10004
    # 10005 ?
    # 10006 ?
    ADVANCED_SHIELD_DEVICE = 10007
    ADVANCED_MISSILE_DEVICE = 10008
    QUICK_TELEPORT = 10009
    # 2000* ... modifiers that affect all units?
    ADVANDED_DEFENSIVE_TACTICS = 20001
    ADVANCED_OFFENSIVE_TACTICS = 20002
    EFFICIENT_TECH_RESEARCH = 20003
    ADVANCED_POWER_SYSTEM = 20004
    # 20005 ?
    ADVANCED_TARGETING_SYSTEM = 20006
    SUPPLY_ENHANCEMENT = 20007
    # 20008 - 20021 ?
    EFFICIENT_GIANT_MANUFACTURING = 20022
    EFFICIENT_LIGHT_MANUFACTURING = 20023

    # 3xxxx - Unit modifiers
    # 301 Fortress
    # 30101 ?
    ASSAULT_FORTRESS = 30102
    # 30103 ?
    # 30104 is deprecated?
    EXTENDED_RANGE_FORTRESS = 30105
    # 302 Marksman
    EXTENDED_RANGE_MARKSMAN = 30201
    SMART_MARKSMAN = 30202
    SUBSIDIZED_MARKSMAN = 30203
    ELITE_MARKSMAN = 30204
    # 303 Vulcan
    EXTENDED_RANGE_VULCAN = 30301
    ASSAULT_VULCAN = 30302
    # 304 Melting Point
    ASSAULT_MELTING_POINT = 30401
    IMPROVED_MELTING_POINT = 30402
    MASS_PRODUCED_MELTING_POINT = 30403
    # 305 Rhino
    MASS_PRODUCED_RHINO = 30501
    BERSERK_RHINO = 30502
    ELITE_RHINO = 30503
    # 306 Wasp
    MASS_PRODUCED_WASP = 30601
    IMPROVED_WASP = 30602
    # 30603 ?
    ELITE_WASP = 30604
    # 307 Mustang
    SUBSIDIZED_MUSTANG = 30701
    FORTIFIED_MUSTANG = 30702
    ELITE_MUSTANG = 30703
    # 308 Steel Ball
    SUBSIDIZED_STEEL_BALL = 30801
    # 30802 ?
    IMPROVED_STEEL_BALL = 30803
    ELITE_STEEL_BALL = 30804
    # 309 Fang
    ELITE_FANG = 30901
    ASSAULT_FANG = 30902
    # 310 Crawler
    SUBSIDIZED_CRAWLER = 31001
    ELITE_CRAWLER = 31002  # Note that this is also a battlefield power
    # 311 Overlord
    FORTIFIED_OVERLORD = 31101
    MASS_PRODUCED_OVERLORD = 31102
    # 31103 ?
    IMPROVED_OVERLORD = 31104
    # 312 Stormcaller
    ASSAULT_STORMCALLER = 31201
    EXTENDED_RANGE_STORMCALLER = 31202
    SUBSIDIZED_STORMCALLER = 31203
    # 31204 ?
    ELITE_STORMCALLER = 31205
    # 313 Sledgehammmer
    MASS_PRODUCED_SLEDGEHAMMER = 31301  # Free
    EXTENDED_RANGE_SLEDGEHAMMER = 31302
    # 31303 ?
    IMPROVED_SLEDGEHAMMER = 31304
    ELITE_SLEDGEHAMMER = 31305
    # 314 Hacker
    # 31401 ?
    FORTIFIED_HACKER = 31402
    ELITE_HACKER = 31403
    # 315 Arclight
    SUBSIDIZED_ARCLIGHT = 31501
    SMART_ARCLIGHT = 31502
    FORTIFIED_ARCLIGHT = 31503
    # 31504 is something deprecated?
    ELITE_ARCLIGHT = 31505
    # 316 Phoenix
    MASS_PRODUCED_PHOENIX = 31601
    EXTENDED_RANGE_PHOENIX = 31602
    IMRPOVED_PHOENIX = 31603
    ELITE_PHOENIX = 31604
    # 317 War Factory
    EXTENDED_RANGE_WAR_FACTORY = 31701
    IMRPOVED_WAR_FACTORY = 31702
    # 318 Wraith
    MASS_PRODUCED_WRAITH = 31801
    IMPROVED_WRAITH = 31802
    # 319 Scorpion
    ASSAULT_SCORPION = 31901
    MASS_PRODUCED_SCORPION = 31902
    IMPROVED_SCORPION = 31903
    # 321 Sabertooth
    EXTENDED_RANGE_SABERTOOTH = 32101
    MASS_PRODUCED_SABERTOOTH = 32102
    IMPROVED_SABERTOOTH = 32103
    # 323 Sandworm
    IMPROVED_SANDWORM = 32301
    MASS_PRODUCED_SANDWORM = 32302
    # 324 Tarantula
    IMPROVED_TARANTULA = 32401
    ELITE_TARANTULA = 32402
    # 325 Phantom Ray
    EXTENDED_RANGE_PHANTOM_RAY = 32501

    # Deprecated?
    XXX_UNKOWN_ARCLIGHT = 31504
    XXX_UNKNOWN_FORTRESS = 30104

    @classmethod
    def parse(cls, id_: str):
        try:
            return cls(int(id_))
        except ValueError:
            first_three_digits = int(id_[:3])
            if first_three_digits == 130:
                return Item(int(id_))
            elif id_[0] == '3' and len(id_) == 5:
                unit = Unit(int(id_[1:3]))
                raise ValueError(f'[red]Unknown Unit buff {id_} for {unit}[/red]')
            elif '0000' in id_ or id_ == '1200013':
                try:
                    return CommanderSkill(int(id_))
                except ValueError:
                    return f'{id_} is an unknown battlefield power.'
            elif first_three_digits in CONFIRMED_UNIT_REINFORCEMENTS:
                rank = int(id_[4])
                amount = int(id_[3])
                assert amount, id_  # This is important!
                unit = Unit(int(id_[5:]))
                return f'{amount} x Rank {rank} {unit}'
            else:
                raise ValueError(f'Unknown reinforcement id: {id_}')


class TowerTech(NamedEnum):
    # From left to right.
    RAPID_RESUPPLY = 1
    MASS_RECRUITMENT = 3
    ELITE_RECRUITMENT = 4
    ENHANCED_RANGE = 5
    HIGH_MOBILITY = 6
    XXX_WAS_NUKE_IN_BETA = 2


class Specialist(NamedEnum):
    """ """

    _NONE = -1
    SUPPLY = 10002
    QUICK_SUPPLY = 10010
    MISSILE = 10011
    AMPLIFY = 10013
    TRAINING = 10014
    _SURVIVAL_PLAYER = 20003
    GIANT = 20005
    AERIAL = 20021
    SPEED = 20024
    MARKSMAN = 20029
    ELITE = 20032
    RHINO = 20033
    COST_CONTROL = 20034
    FORTIFIED = 20035
    SABERTOOTH = 20036
    FARSEER = 20037  # Not in game in version 1706.
    FIRE_BADGER = 20038
    TYPHOON = 20039
    _SURVIVAL_TEAMMATE = 31603

    def __str__(self):
        if self.name.startswith('_'):
            return 'None'
        else:
            return f'{self.name.replace("_", " ").title()} Specialist'

    __rich__ = __str__


class Tower(NamedEnum):
    RESEARCH_CENTER = 0
    COMMAND_CENTER = 1


class UnitTech(NamedEnum):
    # Alphabetically numerical order, sort-of. Just see below, it makes the _most_ sense.
    INVALID = -1  # To mark discontinued techs in old replay files.
    # 1 ???
    PORTABLE_SHIELD = 2  # Fang / 209
    ENERGY_ABSORPTION = 3  # Melting Point / 304
    HIGH_EXPLOSIVE_AMMO = 4
    GROUND_SPECIALIZATION = 5  # Wasp / 506
    DAMAGE_SHARING = 6  # Sledgehamer / 613
    DOUBLE_SHOT = 7  # Sabertooth / 721, "Burst mode" on Farseer / 726a. "Saturation bombardment" on Mountain / 72002
    NAPALM = 8  # Fire Badger / 820, Also "Incendiary bomb" for Stormcaller / 812
    FIELD_MAINTENANCE = 9  # "Burrow maintenance" on Sandworm / 923
    BARRIER = 10  # Fortress / 1001
    ANTI_AIR_BARRAGE = 11  # Fortress / 1105
    # All 12* summon something.
    BEST_PARTNER = 12  # Vulcan / 1203, Overlord / 1112
    PHOENIX_PRODUCTION = 120  # War factory / 12017
    CRAWLER_PRODUCTION = 1204  # Melting point / 1204
    STEEL_BALL_PRODUCTION = 121  # Death knell / 1202001, War Factory / 12117
    SLEDGEHAMMER_PRODUCTION = 122  # War factory / 12217
    # All 13* are mechanical division.
    MECHANICAL_DIVISION_TO_CRAWLERS = 13
    MECHANICAL_DIVISION_TO_LARVAES = 130  # Sandworm / 13023
    # 14 ???
    # 15 ???
    JUMP_DRIVE = 16  # Wasp / 1606
    ENHANCED_CONTROL = 17  # Hacker / 1714
    EMP = 18  # Farseer / 1826, Marksman 1802
    # 19 ???
    # 20 ???
    # 21 ???
    # 22 ???
    WRECKAGE_RECYCLING = 23  # Rhino / 2305
    FORTIFIED_TARGET_LOCK = 24  # Steel Ball / 2408
    POWER_ARMOR = 25  # Rhino / 2305
    SUBTERRANEAN_BLITZ = 26  # Crawler / 2610
    # 27 ???
    FINAL_BLITZ = 28  # Rhino / 2808
    QUANTUM_REASSEMBLY = 29  # Phoenix / 2916
    ARMOR_ENHANCEMENT = 30
    ANTI_AIRCRAFT_AMMUNITION = 31  # Tarantula / 3124
    AERIAL_SPECIALIZATION = 32  # Mustang / 3207
    ANTI_MISSILE = 33  # Mustang / 3307
    EFFICIENT_MAINTENANCE = 34  # Mountain / 342002
    LOOSE_FORMATION = 35  # Crawler / 3510
    # 36 ???
    SANDSTORM = 37  # Sandworm / 3723
    STRIKE = 38  # Sandworm / 3823
    STEALTH_CLOAK = 39  # Phantom Ray / 3925
    CHAIN = 40  # Raiden / 4027
    # 41 ???
    FIRE_EXTINGUISHER = 42  # Hound / 4228
    # 43 ???
    AERIAL_MODE = 44  # Void Eye / 4430
    SIEGE_MODE = 100  # Scorpion / 10019
    # 101 ???
    RANGE = 102  # Fire badger / 10220, Mustang / 10207, Sniper / 10202, Sabertooth / 10221, Phantom Ray / 10225
    FIELD_MAINTENANCE_SABER = 103  # Sabertooth / 10321
    # 104 ???
    MECHANICAL_RAGE_CRAWLER = 105  # Crawler / 10510
    ARMOR_PIERCING_BULLETS_OR_SCORCHING_FIRE = 106  # Fang / 10609, Vulcan / 10603, Fire Badger / 10620
    IMPACT_DRILL = 107  # Crawler / 10710
    ELITE_MARKSMAN = 108  # Marksman / 10802
    CHARGED_SHOT = 109 # Also HE ammo for Stormcaller.
    # Now these just get weird ..., "the 110-series"
    OIL_BOMB = 110  # Phantom ray / 11025
    ROCKET_PUNCH = 1102  # Fortress / 110201
    ELECTROMAGNETIC_BARRAGE = 1106  # Melting point / 1106
    ENERGY_DIFFRACTION = 1107  # Melting point / 1107 (Sic!)
    OVERLORD_ARTILLERY = 1108  # Overlord / 1108
    WHIRLWIND = 1109  # Rhino / 1109
    MECHANICAL_RAGE = 3022
    LAUNCHER_OVERLOAD = 10317
    STICKY_OIL_BOMB = 11010  # Vulcan / 11010a
    MULTI_CONTROL = 11014
    HOMING_MISSILE = 11022
    INCENDIARY_BOMB = 11028
    DARK_COMPANION = 12029
    ACID_ATTACK = 180519  # Scorpion / 180519
    FLOATING_ARTILLERY_ARRAY = 110181  # Wraith / 110118
    SECONDARY_ARMAMENT = 110211  # Sabertooth / 110211
    FORK = 110271 # Raiden / 110271
    SWARM_MISSILES = 110291  # Abyss / 110291 -- wtf is that trailing 1
    EXTENDED_RANGE_AMMO = 1032002
    GUN_LAUNCHED_MISSILE = 11020021  # Mountain / 11020021
    XXX_DEATH_KNELL_LAST_ONE = 11020012 # Death knell / 11020012
    # The 18-series
    REPLICATE = 1801  # Crawler / 180110
    IGNITE = 1802  # Fang / 180209
    PHOTON_EMISSION = 1803  # Overlord / 180311
    SUPPRESSION = 1804  # Void Eye "Suppression shots" / 180430, Wraith "Suppression beam" 180418
    SCANNING_RADAR = 1805  # Farseer / 180526
    EMP_ARMOR = 180530

@dataclasses.dataclass
class Tech:
    unit: Unit
    tech: UnitTech

    @staticmethod
    def parse(id_: str, chosen_unit=None):
        match id_:
            case '1105':
                tech = UnitTech.ANTI_AIR_BARRAGE
                unit = Unit.FORTRESS
            case '1001':
                tech = UnitTech.BARRIER
                unit = Unit.FORTRESS
            case '905':
                tech = UnitTech.FIELD_MAINTENANCE
                unit = Unit.RHINO
            case '921':
                raise ValueError(id_)
            case '1106':
                tech = UnitTech.ELECTROMAGNETIC_BARRAGE
                unit = Unit.MELTING_POINT
            case '1107':
                tech = UnitTech.ENERGY_DIFFRACTION
                unit = Unit.MELTING_POINT
            case '1108':
                tech = UnitTech.OVERLORD_ARTILLERY
                unit = Unit.OVERLORD
            case '1109':
                tech = UnitTech.WHIRLWIND
                unit = Unit.RHINO
            case '1204':
                tech = UnitTech.CRAWLER_PRODUCTION
                unit = Unit.MELTING_POINT
            case '3022':
                tech = UnitTech.MECHANICAL_RAGE
                unit = Unit.TYPHOON
            case '10317':
                tech = UnitTech.LAUNCHER_OVERLOAD
                unit = Unit.WAR_FACTORY
            case '11010':
                tech = UnitTech.STICKY_OIL_BOMB
                unit = Unit.VULCAN
            case '11014':
                tech = UnitTech.MULTI_CONTROL
                unit = Unit.HACKER
            case '11022':
                tech = UnitTech.HOMING_MISSILE
                unit = Unit.TYPHOON
            case '11028':
                tech = UnitTech.INCENDIARY_BOMB
                unit = Unit.HOUND
            case '12029':
                tech = UnitTech.DARK_COMPANION
                unit = Unit.ABYSS
            case '180519':
                tech = UnitTech.ACID_ATTACK
                unit = Unit.SCORPION
            case '32001':  # Death knell techs shared with Melting Point
                tech = UnitTech(int(id_[:-4]))
                unit = Unit.DEATH_KNELL
            case '110181':
                tech = UnitTech.FLOATING_ARTILLERY_ARRAY
                unit = Unit.WRAITH
            case '110211':
                tech = UnitTech.SECONDARY_ARMAMENT
                unit = Unit.SABERTOOTH
            case '110271':
                tech = UnitTech.FORK
                unit = Unit.RAIDEN
            case '110291':
                tech = UnitTech.SWARM_MISSILES
                unit = Unit.ABYSS
            case '180530':
                tech = UnitTech.EMP_ARMOR
                unit = Unit.VOID_EYE
            case '1022001' | '1022002':  # Range for ;ountain and Death Knell
                tech = UnitTech.RANGE
                unit = Unit(int(id_[-4:]))
            case '1032002':
                tech = UnitTech.EXTENDED_RANGE_AMMO
                unit = Unit.MOUNTAIN
            case '1102001':
                tech = UnitTech.ENERGY_DIFFRACTION
                unit = Unit.DEATH_KNELL
            case '1202001':
                tech = UnitTech.STEEL_BALL_PRODUCTION
                unit = Unit.DEATH_KNELL
            case '11020012':
                tech = UnitTech.XXX_DEATH_KNELL_LAST_ONE
                unit = Unit.DEATH_KNELL
            case '11020021':
                tech = UnitTech.GUN_LAUNCHED_MISSILE
                unit = Unit.MOUNTAIN
            case '11020022' | '10102':  # 10102 dubious.
                tech = UnitTech.INVALID
                unit = Unit.DEPRECATED
            case _:
                if len(id_) > 4 and id_.endswith(('2001', '2002')):
                    unit_id_len = 4
                else:
                    unit_id_len = 2
                tech = UnitTech(int(id_[:-unit_id_len]))
                unit = Unit(int(id_[-unit_id_len:]))
        if chosen_unit is not None:
            assert unit == -1 or chosen_unit == unit, id_
        return Tech(unit=unit, tech=tech)


class CommanderSkill(NamedEnum):
    # 30000x == Damage (?)
    # 90000x == Unit "change" (?)
    # x00002 == Ground effect (?)
    # 120 == Summon, except electromagnetic blast ...
    ACID_BLAST = 500002
    CAN_RECRUIT_RANK_5_CRAWLER = 1200004  # ?
    ELECTROMAGNETIC_BLAST_0 = 200002
    ELECTROMAGNETIC_BLAST_1 = 1200002
    ELECTROMAGNETIC_IMPACT = 200001
    FIELD_RECOVERY = 900001
    INCENDIARY_BOMB = 100002
    INEFFICIENT_RECOVERY = 900002
    INTENSIVE_TRAINING = 1100001
    ION_BLAST = 300006  # ?!
    LIGHTNING_STORM = 300005
    MELTING_POINTS_DESCENT = 1200013
    MISSILE_STRIKE = 300001
    MOBILE_BEACON = 1500002  # From Drop?
    MOBILE_BEACON_BRAWL = 1000002
    MOBILE_BEACON_FROM_TOWER = 1500001
    NUKE = 300004
    ORBITAL_BOMBARDMENT = 300003
    ORBITAL_JAVELIN = 300007
    PHOTON_EMISSION = 200003
    REDEPLOYMENT = 1000001  # ?!
    REDEPLOYMENT_BRAWL = 900003  # Brawl innate only?
    RHINO_DROP = 1200006
    SCORPION_ASSAULT = 1200009
    SHIELD_AIRDROP = 800001
    SMOKE_BOMB = 600002
    STICKY_OIL = 400002
    SUMMON_WRAITH = 1200008
    UNDERGROUND_THREAT = 1200001
    VULCANS_DESCENT = 1200005
    WASP_SWARM = 1200003


class BluePrint(NamedEnum):
    STICKY_OIL = 1
    FIELD_RECOVERY = 2
    MOBILE_BEACON = 3  # ?
    ATTACK_ENHANCEMENT = 4
    DEFENCE_ENHANCEMENT = 5


class Contraption(NamedEnum):
    SHIELD_GENERATOR = 10001
    SENTRY_MISSILE = 20001  # ?
    MISSILE_INTERCEPTOR = 30001  # ?

starting_units = {
    9902: (Unit.SABERTOOTH, Unit.HOUND),
    9894: (Unit.SABERTOOTH, Unit.ARCLIGHT),
    9871: (Unit.MARKSMAN, Unit.SLEDGEHAMMER),
    9893: (Unit.SABERTOOTH, Unit.FANG),
    9897: (Unit.HOUND, Unit.STEEL_BALL),
    9889: (Unit.TARANTULA, Unit.MARKSMAN),
    9873: (Unit.MUSTANG, Unit.CRAWLER),
    9874: (Unit.STEEL_BALL, Unit.FANG),
    9900: (Unit.VOID_EYE, Unit.MUSTANG),
    9877: (Unit.FANG, Unit.SLEDGEHAMMER),
    9891: (Unit.TARANTULA, Unit.CRAWLER),
    9883: (Unit.ARCLIGHT, Unit.STEEL_BALL),
    9885: (Unit.ARCLIGHT, Unit.SLEDGEHAMMER),
    9876: (Unit.FANG, Unit.STORMCALLER),
    9875: (Unit.STEEL_BALL, Unit.CRAWLER),
    9899: (Unit.VOID_EYE, Unit.SLEDGEHAMMER),
    9896: (Unit.HOUND, Unit.MUSTANG),
    9892: (Unit.SABERTOOTH, Unit.CRAWLER),
    9901: (Unit.VOID_EYE, Unit.TARANTULA),
    9884: (Unit.ARCLIGHT, Unit.STORMCALLER),
    9878: (Unit.CRAWLER, Unit.STORMCALLER),
    9879: (Unit.CRAWLER, Unit.SLEDGEHAMMER),
    9890: (Unit.TARANTULA, Unit.FANG),
    9898: (Unit.HOUND, Unit.STORMCALLER),
    9895: (Unit.HOUND, Unit.SLEDGEHAMMER)
}
