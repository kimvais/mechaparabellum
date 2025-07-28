import enum

import stringcase

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
class Unit(enum.IntEnum):
    # 0 + 100 :
    CRAWLER = 10
    MARKSMAN = 2  # ???
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
    WRAITH = 18
    # The following must be 1, 3, 14, 17, 19, 23, 26, and 27
    # 200 + 400: Vulcan, Sandworm, Raiden
    FORTRESS = 1
    MELTING_POINT = 4
    # 200 + 500: Overlord
    # 200 + 800: War Factory, Mountain
    ABYSS = 29
    # 200 drops: Fire Badger, Typhoon
    FIRE_BADGER = 20

    def __str__(self):
        return self.name.replace('_', ' ').title()

class Reinforcements(enum.IntEnum):
    # Units = 10.XRUU, where X is amount, R is rank and UU is unit ID . is probably price?
    # 0000 in string format = spell
    # Unit modifiers = 3UU??
    # Items = 13.+
    ELECTROMAGNETIC_IMPACT = 200001
    HEAVY_ARMOR = 1303000
    INCENDIARY_BOMB = 100002
    LIGHTNING_STORM = 300005
    ORBITAL_BOMBARDMENT = 300003
    MASS_PRODUCED_SLEDGEHAMMER = 31301   # Free
    ASSAULT_STORMCALLER = 31201  #  Free
    MOBILE_BEACON = 1500002
    RANK_1_FIRE_BADGER_X3 = 1043120
    RANK_2_FIRE_BADGER_X2 = 1042220  # 50
    RANK_2_PHANTOM_RAY_X1 = 1062225
    RANK_3_TYPHOON_X1 = 1061322
    RANK_3_WASP_X1 = 103136
    RANK_1_FORTRESS_X2 = 107211  # 150
    SUBSIDIZED_CRAWLER = 31001
    VULCANS_DESCENT = 1200005
    AMPLIFYING_CORE = 13030007 # 150
    ABSORPTION_MODULE = 1309001 # 150


class TowerTechs(enum.IntEnum):
    # MASS_RECRUITMENT = 1100001
    RAPID_RESUPPLY = 1
    HIGH_MOBILITY = 2  # ?
    MASS_RECRUITMENT = 3
    ELITE_RECRUITMENT = 4
    ENHANCED_RANGE = 5


class Specialist(enum.IntEnum):
    TRAINING = 9894  # Arclights and Sabretooths
    RHINO = 9878  # Crawlers and StormCallers

class UnitTech(enum.IntEnum):
    # Range = 102 + UID
    FIRE_BADGER_RANGE = 10220
    PHANTOM_RAY_RANGE = 10225
    MUSTANG_RANGE = 10207
    SNIPER_RANGE = 10202
    PHANTOM_RAY_OIL = 11025   # Oil = 110
    MUSTANG_ANTI_MISSILE = 3307
    SABER_RANGE = 10221

class CommanderSkill(enum.IntEnum):
    INTENSIVE_TRAINING = 1100001
    FIELD_RECOVERY = 900001
    STICKY_OIL = 400002

class BluePrint(enum.IntEnum):
    STICKY_OIL = 1
    FIELD_RECOVERY = 2
    MOBILE_BEACON = 3  # ?
    ATTACK_ENHANCEMENT = 4
    DEFENCE_ENHANCEMENT = 5
