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
    # 200 + 800:
    ABYSS = 29
    WAR_FACTORY = 17
    MOUNTAIN = 2002
    # 200 drops:
    TYPHOON = 22
    FIRE_BADGER = 20
    # Brawl drops
    DEATH_KNELL = 2001

class Item(NamedEnum):
    ABSORPTION_MODULE = 1309001 # 150
    AMPLIFYING_CORE = 13030007 # 150
    BARRIER = 1307001
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
    # Units = 1[01].XRUU, where X is amount, R is rank and UU is unit ID . is probably price?
    # 3xx in Brawl
    # 2xx in Survival
    # 0000 in string format = spell
    # Unit modifiers = 3UU??
    # Items = 130+
    _SKIP = 0
    ADDITIONAL_DEPLOYMENT_SLOT = 10004
    ADVANDED_DEFENSIVE_TACTICS = 20001
    ADVANCED_OFFENSIVE_TACTICS = 20002
    ADVANCED_SHIELD_DEVICE = 10007
    ASSAULT_FANG = 30902
    ASSAULT_FORTRESS = 30102
    ASSAULT_MELTING_POINT = 30401
    ASSAULT_SCORPION = 31901
    ASSAULT_STORMCALLER = 31201  #  Free
    BERSERK_RHINO = 30502
    EFFICIENG_GIANT_MANUFACTURING = 20022
    EFFICIENT_LIGHT_MANUFACTURING = 20023
    EFFICIENT_TECH_RESEARCH = 20003
    ELITE_CRAWLER = 31002
    ELITE_FANG = 30901
    ELITE_HACKER = 31403
    ELITE_MARKSMAN = 30204
    ELITE_MUSTANG = 30703
    ELITE_PHOENIX = 31604
    ELITE_STORMCALLER = 31205
    ELITE_TARANTULA = 32402
    EXTENDED_RANGE_FORTRESS = 30105
    EXTENDED_RANGE_MARKSMAN = 30201
    EXTENDED_RANGE_PHANTOM_RAY = 32501
    EXTENDED_RANGE_PHOENIX = 31602
    EXTENDED_RANGE_SLEDGEHAMMER = 31302
    EXTENDED_RANGE_STORMCALLER = 31202
    FORTIFIED_HACKER = 31402
    FORTIFIED_MUSTANG = 30702
    FORTIFIED_OVERLORD = 31101
    EXTENDED_RANGE_SABERTOOTH = 32101
    IMPROVED_MELTING_POINT = 30402 #
    IMPROVED_OVERLORD = 31104
    IMRPOVED_PHOENIX = 31603
    IMPROVED_SABERTOOTH = 32103
    IMPROVED_SANDWORM = 32301
    IMPROVED_SCORPION = 31903
    IMPROVED_SLEDGEHAMMER = 31304
    IMRPOVED_WAR_FACTORY = 31702
    MASS_PRODUCED_MELTING_POINT = 30403
    MASS_PRODUCED_OVERLORD = 31102
    MASS_PRODUCED_PHOENIX = 31601
    MASS_PRODUCED_RHINO = 30501
    MASS_PRODUCED_SABERTOOTH = 32102
    MASS_PRODUCED_SCORPION = 31902
    MASS_PRODUCED_SLEDGEHAMMER = 31301   # Free
    MASS_PRODUCED_WASP = 30601
    MASS_PRODUCED_WRAITH = 31801
    QUICK_COOLDOWN = 10001
    QUICK_TELEPORT = 10009
    SMART_ARCLIGHT = 31502
    SMART_MARKSMAN = 30202
    SUBSIDIZED_CRAWLER = 31001
    SUBSIDIZED_MARKSMAN = 30203
    SUBSIDIZED_MUSTANG = 30701
    SUBSIDIZED_STEEL_BALL = 30801
    SUBSIDIZED_STORMCALLER = 31203
    SUPER_SUPPLY_ENHANCEMENT = 10003
    SUPPLY_ENHANCEMENT = 20007
    # WASP_SWARM_MAYBE = 13030001 # This is false.
    ADVANCED_TARGETING_SYSTEM = 20006

    @classmethod
    def parse(cls, id_: str):
        try:
            return cls(int(id_))
        except ValueError:
            if len(id_) == 5:
                unit = Unit(int(id_[1:3]))
                raise ValueError(f'[red]Unknown Unit buff {id_} for {unit}[/red]')
            elif '0000' in id_ or id_ == '1200013':
                    try:
                        return CommanderSkill(int(id_))
                    except ValueError:
                        return f'{id_} is an unknown battlefield power.'
            else:
                match int(id_[:3]):
                    # 3xx happens as reinforcement #2 in Brawl
                    # 2xx is in survival
                    # support for those is very much experimental.
                    case 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 202 | 205 | 302 | 303 | 304 | 305 | 306 | 307 | 308 | 309 | 310: # ?
                        rank = int(id_[4])
                        amount = int(id_[3])
                        assert amount, id_   # This is important!
                        unit = Unit(int(id_[5:]))
                        return f'{amount} x Rank {rank} {unit}'
                    case 130:
                        return Item(int(id_))
                    case _:
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
    # 12, 120 and 121 (..and 122 etc?) are all summons.
    ENHANCED_CONTROL = 17  # Hacker / 1714
    ARMOR_ENHANCEMENT = 9
    # Mustang / 3307
    ANTI_MISSILE = 33
    # Mountain / 342002
    EFFICIENT_MAINTENANCE = 34
    # Phantom Ray / 3925
    STEALTH_CLOAK = 39
    # Fang / 10609
    ARMOR_PIERCING_BULLETS = 106
    # Fire badger / 10220, Mustang / 10207, Sniper / 10202, Sabertooth / 10221, Phantom Ray / 10225
    RANGE = 102
    # Rhino / ..05
    WRECKAGE_RECYCLING = 23
    POWER_ARMOR = 25
    FINAL_BLITZ = 28
    # Phantom ray / 11025
    OIL_BOMB = 110  # 110 is Energy Diffraction for Melting Pot and Death Knell, but the Unit ID is 7 in former case :O
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
    # Melting point / 1204
    CRAWLER_PRODUCTION = 1204
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
    # War factory / 12017
    PHOENIX_PRODUCTION = 120
    # Death knell / 1202001, War Factory / 12117
    STEEL_BALL_PRODUCTION = 121
    # War factory / 12217
    SLEDGEHAMMER_PRODUCTION = 122
    # Marksman / 10802
    ELITE_MARKSMAN = 108
    # Vulcan / 1203, Overlord / 1112
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
    # Fortress / 110201
    ROCKET_PUNCH = 1102
    # Crawler / 180110
    REPLICATE = 1801
    # Vulcan / 11010
    STICKY_OIL_BOMB = 11010
    # Wraith / 110118
    FLOATING_ARTILLERY_ARRAY = 110181
    # Overlord / 180311
    PHOTON_EMISSION = 1803
    # Void Eye / 180430
    SUPPRESSION_SHOTS = 1804
    # Abyss / 110291 -- wtf is that trailing 1
    SWARM_MISSILES = 110291


    @classmethod
    def parse(cls, id_: str, chosen_unit):
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
            case '1204':
                tech = cls.CRAWLER_PRODUCTION
                unit = Unit.MELTING_POINT
            case '11010':
                tech = cls.STICKY_OIL_BOMB
                unit = Unit.VULCAN
            case '32001':  # Death knell techs shared with Melting Point
                tech = cls(int(id_[:-4]))
                unit = Unit.DEATH_KNELL
            case '110181':
                tech = cls.FLOATING_ARTILLERY_ARRAY
                unit = Unit.WRAITH
            case '110291':
                tech = cls.SWARM_MISSILES
                unit = Unit.ABYSS
            case '1022001' | '1022002':  # Range for ;ountain and Death Knell
                tech = cls.RANGE
                unit = Unit(int(id_[-4:]))
            case '1102001':
                tech = cls.ENERGY_DIFFRACTION
                unit = Unit.DEATH_KNELL
            case '1202001':
                tech = cls.STEEL_BALL_PRODUCTION
                unit = Unit.DEATH_KNELL
            case _:
                if len(id_) > 4 and id_.endswith(('2001', '2002')):
                    unit_id_len = 4
                else:
                    unit_id_len = 2
                tech = cls(int(id_[:-unit_id_len]))
                unit = Unit(int(id_[-unit_id_len:]))
        assert chosen_unit == unit, id_
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
    MELTING_POINTS_DESCENT = 1200013
    MISSILE_STRIKE = 300001
    MOBILE_BEACON = 1500002  # From Drop?
    MOBILE_BEACON_BRAWL = 1000002
    MOBILE_BEACON_FROM_TOWER = 1500001
    NUKE = 300004
    ORBITAL_BOMBARDMENT = 300003
    ORBITAL_JAVELIN = 300007
    PHOTON_EMISSION = 200003
    REDEPLOYMENT = 900003  # Brawl innate only?
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
