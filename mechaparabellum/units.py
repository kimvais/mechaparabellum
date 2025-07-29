import enum

from asttokens.util import is_starred

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
class NamedEnum(enum.IntEnum):
    def __str__(self):
        return self.name.replace('_', ' ').title()

class Unit(NamedEnum):
    # 0 + 100 :
    CRAWLER = 10
    MARKSMAN = 2
    HOUND = 28
    VOID_EYE = 30
    ARCLIGHT = 15
    FANG = 9  # ?!?
    # 0 + 200
    SLEDGEHAMMER = 13
    STEEL_BALL = 8
    SABERTOOTH = 21
    STORMCALLER = 12
    MUSTANG = 7
    TARANTULA = 24
    # 50 + 200:
    WASP = 6
    RHINO = 5
    PHOENIX = 16
    PHANTOM_RAY = 25
    # 100 + 200: Hacker
    # 50 + 300: Wraith, Scorpion, Farseer
    FARSEER = 26
    WRAITH = 18
    # The following must be 1, 3, 14, 17, 19, 23, 26, and 27
    # 200 + 400: Vulcan, Sandworm, Raiden
    RAIDEN = 27
    FORTRESS = 1
    SANDWORM = 23
    MELTING_POINT = 4
    # 200 + 500:
    OVERLORD = 11
    # 200 + 800: War Factory, Mountain
    ABYSS = 29
    # 200 drops:
    TYPHOON = 22
    FIRE_BADGER = 20

class Item(NamedEnum):
    ABSORPTION_MODULE = 1309001 # 150
    AMPLIFYING_CORE = 13030007 # 150
    HASTE_MODULE = 13030005
    HEAVY_ARMOR = 13030002
    IMPROVED_FIREPOWER_CONTROL_SYSTEM = 13030003  # ???
    LASER_SIGHTS = 13030001
    NANO_REPAIR_KIT = 13020001
    SMALL_AMPLIFYING_CORE = 13030009
    STEEL_BALL_PRODUCTION_LINE = 1306003

class Reinforcement(NamedEnum):
    # Units = 10.XRUU, where X is amount, R is rank and UU is unit ID . is probably price?
    # 0000 in string format = spell
    # Unit modifiers = 3UU??
    # Items = 130+
    ADDITIONAL_DEPLOYMENT_SLOT = 10004
    ADVANDED_DEFENSIVE_TACTICS = 20001
    ASSAULT_STORMCALLER = 31201  #  Free
    EFFICIENT_TECH_RESEARCH = 20003
    ELITE_CRAWLER = 31002
    ELITE_HACKER = 31403
    FORTIFIED_OVERLORD = 31101
    EXTENDED_RANGE_SABERTOOTH = 32101
    IMPROVED_MELTING_POINT = 30402 #
    MASS_PRODUCED_SLEDGEHAMMER = 31301   # Free
    MASS_PRODUCED_RHINO = 30501
    ORBITAL_BOMBARDMENT = 300003
    QUICK_COOLDOWN = 10001
    QUICK_TELEPORT = 10009
    SUBSIDIZED_CRAWLER = 31001
    SUBSIDIZED_STEEL_BALL = 30801
    SUPER_SUPPLY_ENHANCEMENT = 10003
    VULCANS_DESCENT = 1200005
    WASP_SWARM_MAYBE = 13030001 # This is false.
    XXX = 20006

    @classmethod
    def parse(cls, id_: str):
        try:
            return cls(int(id_))
        except ValueError:
            if len(id_) == 5:
                unit = Unit(int(id_[1:3]))
                return f'Unknown Unit buff {id_} for {unit}'
            else:
                match int(id_[:3]):
                    case 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 | 109:  # ?
                        rank = int(id_[4])
                        amount = int(id_[3])
                        unit = Unit(int(id_[5:]))
                        return f'{amount} x Rank {rank} {unit}'
                    case 130:
                        return Item(int(id_))
                    case _:
                        if '0000' in id_:
                            try:
                                return CommanderSkill(int(id_))
                            except ValueError:
                                return f'{id_} is an unknown battlefield power.'
                        else:
                            raise ValueError(f'Unknown reinforcement id: {id_}')


class TowerTech(NamedEnum):
    RAPID_RESUPPLY = 1
    HIGH_MOBILITY = 2  # ?
    MASS_RECRUITMENT = 3
    ELITE_RECRUITMENT = 4
    ENHANCED_RANGE = 5


class Specialist(NamedEnum):
    TRAINING = 9894
    RHINO = 9878
    AMPLIFY = 9897  # And 9884?
    FORTIFIED = 9896
    TYPHOON = 9871  # 9875
    MARKSMAN = 9876
    COST_CONTROL = 9879  # Typhoon?!
    SABERTOOTH = 9893



class Tower(NamedEnum):
    RESEARCH_CENTER = 0  # ?
    COMMAND_CENTER = 1


class UnitTech(NamedEnum):
    # Mustang / 3307
    ANTI_MISSILE = 33
    # Fire badger / 10220, Mustang / 10207, Sniper / 10202, Sabertooth / 10221, Phantom Ray / 10225
    RANGE = 102
    # Rhino / ..05
    WRECKAGE_RECYCLING = 23
    POWER_ARMOR = 25
    FINAL_BLITZ = 28
    # Phantom ray / 11025
    OIL_BOMB = 110
    # Steel Ball / 2408, 1308
    FORTIFIED_TARGET_LOCK = 24
    MECHANICAL_DIVISION = 13
    # Mustang / 3207
    AERIAL_SPECIALIZATION = 32
    # Fortress / 1105
    ANTI_AIR_BARRAGE = 11
    # Fortress / 1001
    BARRIER = 10
    # Sabretooth / 10321
    FIELD_MAINTENANCE = 103
    # Farseer / 1826
    ELECTROMAGNETIC_EXPLOSION = 18
    # Typhoon / 3022
    MECHANICAL_RAGE_TYPHOON = 30
    # Crawler / 10510
    MECHANICAL_RAGE_CRAWLER = 105
    # Melting point / 1107 (Sic!)
    ENERGY_DIFFRACTION = 1107
    # Phoenix / 2916
    QUANTUM_REASSEMBLY = 29
    # Hound / 4228
    FIRE_EXTINGUISHER = 42
    CHARGED_SHOT = 109
    # Crawler / 2610
    SUBTERRANEAN_BLITZ = 26
    # Melting Point / 304
    ENERGY_ABSORPTION = 3

    @classmethod
    def parse(cls, id_: str):
        match id_:
            case '1105':
                tech = cls.ANTI_AIR_BARRAGE
                unit = Unit.FORTRESS
            case '1001':
                tech = cls.BARRIER
                unit = Unit.FORTRESS
            case '905':
                tech = cls.FIELD_MAINTENANCE
                unit = Unit.RHINO
            case '1107':
                tech = cls.ENERGY_DIFFRACTION
                unit = Unit.MELTING_POINT
            case _:
                tech = cls(int(id_[:-2]))
                unit = Unit(int(id_[-2:]))

        return tech, unit

class CommanderSkill(NamedEnum):
    INTENSIVE_TRAINING = 1100001
    FIELD_RECOVERY = 900001
    STICKY_OIL = 400002
    MOBILE_BEACON = 1500002
    MASS_RECRUITMENT = 1100001
    ELECTROMAGNETIC_IMPACT = 200001
    SHIELD_AIRDROP = 800001
    ACID_BLAST = 500002
    PHOTON_EMISSION = 200003
    XXX = 300006
    XXX_SHIELD_AIRDROP = 1000001 # ?!

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
