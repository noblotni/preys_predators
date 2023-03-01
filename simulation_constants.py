"""Contain simulation constants."""

PERCENT_TO_PROBA = 1 / 100

# Default constants
# Number of sheeps at the first step
DEFAULT_INIT_NB_SHEEPS = 100
# Number of wolves at the first step
DEFAULT_INIT_NB_WOLVES = 50
# Sheep reproduction rate (%)
DEFAULT_SHEEP_REPRODUCTION_RATE = 4
# Wolf reproduction rate (%)
DEFAULT_WOLF_REPRODUCTION_RATE = 5
# Energy gained by a sheep from eating grass
DEFAULT_SHEEP_GAIN_FROM_GRASS = 10
# Energy gained by a wolf from eating a sheep
DEFAULT_WOLF_GAIN_FROM_SHEEP = 20
# Energy lost by a sheep when moving
# from a case of the grid to another
DEFAULT_SHEEP_MOVE_LOSS = 2
# Energy lost by a wolf when moving
# from a case to another
DEFAULT_WOLF_MOVE_LOSS = 6

# Bounds
MIN_INIT_NB_SHEEPS = 10
MAX_INIT_NB_SHEEPS = 200
MIN_INIT_NB_WOLVES = 10
MAX_INIT_NB_WOLVES = 200
MIN_SHEEP_GAIN_FROM_GRASS = 1
MAX_SHEEP_GAIN_FROM_GRASS = 30
MIN_WOLF_GAIN_FROM_SHEEP = 1
MAX_WOLF_GAIN_FROM_SHEEP = 30
# Minimal value of the sheeps' reproduction rate (%)
MIN_SHEEP_REPRODUCTION_RATE = 1
# Maximal value of the sheeps' reproduction rate (%)
MAX_SHEEP_REPRODUCTION_RATE = 100
# Minimal value of the wolves' reproduction rate (%)
MIN_WOLF_REPRODUCTION_RATE = 1
# Maximal value of the wolves' reproduction rate (%)
MAX_WOLF_REPRODUCTION_RATE = 100
