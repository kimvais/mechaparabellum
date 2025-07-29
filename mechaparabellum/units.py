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
    FANG = 9
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
    # 100 + 200:
    HACKER = 14
    # 50 + 300:
    FARSEER = 26
    WRAITH = 18
    SCORPION = 19
    # 200 + 400:
    VULCAN = 3
    RAIDEN = 27
    FORTRESS = 1
    SANDWORM = 23
    MELTING_POINT = 4
    # 200 + 500:
    OVERLORD = 11
    # 200 + 800: Mountain
    ABYSS = 29
    WAR_FACTORY = 17
    # 200 drops:
    TYPHOON = 22
    FIRE_BADGER = 20

class Item(NamedEnum):
    ABSORPTION_MODULE = 1309001 # 150
    AMPLIFYING_CORE = 13030007 # 150
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
    DEPLOYMENT_MODULE = 13040001  # ???

class Reinforcement(NamedEnum):
    # Units = 10.XRUU, where X is amount, R is rank and UU is unit ID . is probably price?
    # 0000 in string format = spell
    # Unit modifiers = 3UU??
    # Items = 130+
    _SKIP = 0
    ADDITIONAL_DEPLOYMENT_SLOT = 10004
    ADVANDED_DEFENSIVE_TACTICS = 20001
    ASSAULT_FANG = 30902
    ASSAULT_MELTING_POINT = 30401
    ASSAULT_SCORPION = 31901
    ASSAULT_STORMCALLER = 31201  #  Free
    EFFICIENT_LIGHT_MANUFACTURING = 20023
    EFFICIENT_TECH_RESEARCH = 20003
    ELITE_CRAWLER = 31002
    ELITE_FANG = 30901
    ELITE_HACKER = 31403
    ELITE_MUSTANG = 30703
    ELITE_PHOENIX = 31604
    EXTENDED_RANGE_PHANTOM_RAY = 32501
    EXTENDED_RANGE_PHOENIX = 31602
    EXTENDED_RANGE_SLEDGEHAMMER = 31302
    EXTENDED_RANGE_STORMCALLER = 31202
    FORTIFIED_HACKED = 31402
    FORTIFIED_OVERLORD = 31101
    EXTENDED_RANGE_SABERTOOTH = 32101
    IMPROVED_MELTING_POINT = 30402 #
    IMPROVED_OVERLORD = 31104
    MASS_PRODUCED_RHINO = 30501
    MASS_PRODUCED_SCORPION = 31902
    MASS_PRODUCED_SLEDGEHAMMER = 31301   # Free
    MASS_PRODUCED_WASP = 30601
    MASS_PRODUCED_WRAITH = 31801
    QUICK_COOLDOWN = 10001
    QUICK_TELEPORT = 10009
    SMART_MARKSMAN = 30202
    SUBSIDIZED_CRAWLER = 31001
    SUBSIDIZED_MARKSMAN = 30203
    SUBSIDIZED_STEEL_BALL = 30801
    SUBSIDIZED_STORMCALLER = 31203
    SUPER_SUPPLY_ENHANCEMENT = 10003
    SUPPLY_ENHANCEMENT = 20007
    WASP_SWARM_MAYBE = 13030001 # This is false.
    ADVANCED_TARGETING_SYSTEM = 20006

    @classmethod
    def parse(cls, id_: str):
        try:
            return cls(int(id_))
        except ValueError:
            if len(id_) == 5:
                unit = Unit(int(id_[1:3]))
                raise ValueError(f'[red]Unknown Unit buff {id_} for {unit}[/red]')
            else:
                match int(id_[:3]):
                    case 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 112:  # ?
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
    TRAINING = 9894 # 9876
    RHINO = 9899 #, 9878 (?)
    AMPLIFY = 9897  # And 9884?
    FORTIFIED = 9896  # 9890
    GIANT = 9892 # also marksman
    TYPHOON = 9891  # 9871,  9875, 9873, 9878(?)
    MARKSMAN = 9892 #, 9876 - also Giant
    COST_CONTROL = 9889 #, 9879  # Typhoon?!, # 9891, 9889
    SABERTOOTH = 9893
    QUICK_SUPPLY = 9885 #, 9877, 9900
    ELITE = 9884
    FIRE_BADGER = 9884 #, 9889 - See COST_CONTROL!


class Tower(NamedEnum):
    RESEARCH_CENTER = 0  # ?
    COMMAND_CENTER = 1


class UnitTech(NamedEnum):
    ARMOR_ENHANCEMENT = 9
    # Mustang / 3307
    ANTI_MISSILE = 33
    # Fang / 10609
    ARMOR_PIERCING_BULLETS = 106
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
    MECHANICAL_DIVISION_TO_CRAWLERS = 13
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
    # Fang / 209
    PORTABLE_SHIELD = 2
    # Wasp / 1606
    JUMP_DRIVE = 16
    # Sandworm / 13023
    MECHANICAL_DIVISION_TO_LARVAES = 130
    # War factory / 12117, 12017
    PHOENIX_PRODUCTION = 120
    STEEL_BALL_PRODUCTION = 121
    # Marksman / 10802
    ELITE_MARKSMAN = 108
    # Vulcan / 1203
    BEST_PARTNER = 12
    # Fire Badger / 820
    NAPALM = 8
    # Sabertooth / 721
    DOUBLE_SHOT = 7
    # Wasp / 506
    GROUND_SPECIALIZATION = 5
    # Farseer / 180526
    SCANNING_RADAR = 1805
    # Scorpion / 10019
    SIEGE_MODE = 100
    # Raiden / 4027
    CHAIN = 40
    # Abyss / 110291 -- wtf is that trailing 1
    SWARM_MISSILES = 110291

    @classmethod
    def parse(cls, id_: str):
        match id_:
            case '3003':  # !?
                tech = cls.ARMOR_ENHANCEMENT
                unit = Unit.VULCAN
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
            case '110291':
                tech = cls.SWARM_MISSILES
                unit = Unit.ABYSS
            case _:
                tech = cls(int(id_[:-2]))
                unit = Unit(int(id_[-2:]))

        return tech, unit


class CommanderSkill(NamedEnum):
    ACID_BLAST = 500002
    ELECTROMAGNETIC_BLAST_0 = 200002
    ELECTROMAGNETIC_BLAST_1 = 1200002
    ELECTROMAGNETIC_IMPACT = 200001
    FIELD_RECOVERY = 900001
    INCENDIARY_BOMB = 100002
    INTENSIVE_TRAINING = 1100001
    ION_BLAST = 300006  # ?!
    LIGHTNING_STORM = 300005
    MISSILE_STRIKE = 300001
    MOBILE_BEACON = 1500002  # From Drop?
    MOBILE_BEACON_FROM_TOWER = 1500001
    ORBITAL_BOMBARDMENT = 300003
    ORBITAL_JAVELIN = 300007
    PHOTON_EMISSION = 200003
    RHINO_DROP = 1200006
    SHIELD_AIRDROP = 800001
    SMOKE_BOMB = 600002
    STICKY_OIL = 400002
    UNDERGROUND_THREAT = 1200001
    VULCANS_DESCENT = 1200005
    WASP_SWARM = 1200003
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
