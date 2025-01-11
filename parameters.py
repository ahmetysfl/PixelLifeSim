# Parameters
FIXED_STEP_DURATION = 0.1  # Each step is 0.2 seconds
MAX_CREATURES = 80
MAX_ENERGY_CAPACITY = 200
MIN_ENERGY_CAPACITY = 1
GENERAL_ENERGY_CONSUMPTION = 8
GENERAL_ENERGY_PRODUCTION = 10
GENERAL_GENETIC_COST = 0.4

CREATURE_SIZE_MAX = 10  # Creature size
CREATURE_SIZE_MIN = 5  # Creature size
MUTATION_RATE = 0.1  # Mutation rate

MATURITY_LEVEL_MAX = 20
MATURITY_LEVEL_MIN = 5
AGING_LEVEL_STARTS = MATURITY_LEVEL_MAX * 3

#Yaratık beyin yapısı
BRAIN_LAYER1_SIZE = 16
BRAIN_LAYER2_SIZE = 8
BRAIN_LEARNING_RATE = 0.05

CONSUMPTION_RATE_MAX = 1
CONSUMPTION_RATE_MIN = 0.2

PRODUCTION_RATE_MAX = 0.8
PRODUCTION_RATE_MIN = 0

RESOURCE_SHARE_RATIO_MAX = 1.0  # Maximum resource share ratio
RESOURCE_SHARE_RATIO_MIN = 0.0  # Minimum resource share ratio


# Action Zone Ratio Parameters
ACTION_ZONE_RATIO_MAX = 1
ACTION_ZONE_RATIO_MIN = 0
ACTION_ZONE_MAX = CREATURE_SIZE_MAX * 6

# Yeni parametreler
CONSUME_OTHER_CREATURES_RATIO_MAX = 1.0  # Maximum tüketme oranı
CONSUME_OTHER_CREATURES_RATIO_MIN = 0.0  # Minimum tüketme oranı

# Action Cost Calculation Weights
ACTION_COST_GENERAL_RATIO = GENERAL_ENERGY_CONSUMPTION * 0.1  # Üretim oranının eylem maliyetine katkısı
ACTION_COST_PRODUCTION_RATE_WEIGHT = 1  # Üretim oranının eylem maliyetine katkısı
ACTION_COST_ENERGY_CAPACITY_WEIGHT = 2  # Enerji kapasitesinin eylem maliyetine katkısı
ACTION_COST_ACTION_ZONE_WEIGHT = 1       # Eylem bölgesi oranının eylem maliyetine katkısı
ACTION_COST_CONSUME_OTHERS_WEIGHT = 1.5   # Diğer canlıları tüketme oranının eylem maliyetine katkısı
ACTION_COST_RESOURCE_SHARE_WEIGHT = 0.5  # Kaynak paylaşım oranının eylem maliyetine katkısı


# Crowded Zone Parameters
CROWDED_ZONE_THRESHOLD = 20  # Kalabalık bölge için minimum yaratık sayısı
CROWDED_ZONE_RADIUS = CREATURE_SIZE_MAX * 5  # Kalabalık bölge yarıçapı

# Screen dimensions
WIDTH, HEIGHT = 400, 300

PLOT_PAUSE = 0.2
