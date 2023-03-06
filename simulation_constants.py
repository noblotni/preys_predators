"""Contain simulation constants."""
from pathlib import Path
import matplotlib as mpl

PERCENT_TO_PROBA = 1 / 100
SECOND_TO_MSECOND = 1000

# Default constants
# Model speed (%)
DEFAULT_MODEL_SPEED = 100
# Number of sheeps at the first step
DEFAULT_INIT_NB_SHEEPS = 100
# Number of wolves at the first step
DEFAULT_INIT_NB_WOLVES = 50
# Sheep reproduction rate (%)
DEFAULT_SHEEP_REPRODUCTION_RATE = 4
# Wolf reproduction rate (%)
DEFAULT_WOLF_REPRODUCTION_RATE = 5
# Energy gained by a sheep from eating grass
DEFAULT_SHEEP_GAIN_FROM_GRASS = 13
# Energy gained by a wolf from eating a sheep
DEFAULT_WOLF_GAIN_FROM_SHEEP = 10
# Number of steps without grass
# on a patch if eaten by a sheep
DEFAULT_GRASS_REGROWTH_TIME = 30
# Boolean to add a sickness among the sheeps
DEFAULT_ADD_SICKNESS = False

# GUI
# Bounds of the parameters which
# can be set in the GUI
<<<<<<< HEAD
MIN_MODEL_SPEED = 1
MAX_MODEL_SPEED = 100
=======
>>>>>>> 2034002 (Improve grid plot.)
MIN_INIT_NB_SHEEPS = 1
MAX_INIT_NB_SHEEPS = 200
MIN_INIT_NB_WOLVES = 1
MAX_INIT_NB_WOLVES = 200
MIN_GRASS_REGROWTH_TIME = 1
MAX_GRASS_REGROWTH_TIME = 100
MIN_SHEEP_GAIN_FROM_GRASS = 1
MAX_SHEEP_GAIN_FROM_GRASS = 50
MIN_WOLF_GAIN_FROM_SHEEP = 1
MAX_WOLF_GAIN_FROM_SHEEP = 100
# Minimal value of the sheeps' reproduction rate (%)
MIN_SHEEP_REPRODUCTION_RATE = 1
# Maximal value of the sheeps' reproduction rate (%)
MAX_SHEEP_REPRODUCTION_RATE = 20
# Minimal value of the wolves' reproduction rate (%)
MIN_WOLF_REPRODUCTION_RATE = 1
# Maximal value of the wolves' reproduction rate (%)
MAX_WOLF_REPRODUCTION_RATE = 20

# Sheeps image for the GUI
ASCII_SHEEPS_PATH = Path("./assets/ascii_sheeps.png")


# Constants for the colors of the pixels on the grid plot
EMPTY_CASE = 0
WOLF = 1
<<<<<<< HEAD
HEALTHY_SHEEP = 2
GREEN_PATCH = 3
BROWN_PATCH = 4
SICK_SHEEP = 5
EMPTY_CASE_COLOR = "black"
WOLF_COLOR = "pink"
HEALTHY_SHEEP_COLOR = "white"
SICK_SHEEP_COLOR = "yellow"
GREEN_PATCH_COLOR = "green"
BROWN_PATCH_COLOR = "brown"
GRID_PLOT_CMAP = mpl.colors.ListedColormap(
    [
        EMPTY_CASE_COLOR,
        WOLF_COLOR,
        HEALTHY_SHEEP_COLOR,
        GREEN_PATCH_COLOR,
        BROWN_PATCH_COLOR,
        SICK_SHEEP_COLOR,
    ]
=======
SHEEP = 2
GREEN_PATCH = 3
BROWN_PATCH = 4
EMPTY_CASE_COLOR = "black"
WOLF_COLOR = "pink"
SHEEP_COLOR = "white"
GREEN_PATCH_COLOR = "green"
BROWN_PATCH_COLOR = "brown"
GRID_PLOT_CMAP = mpl.colors.ListedColormap(
    [EMPTY_CASE_COLOR, WOLF_COLOR, SHEEP_COLOR, GREEN_PATCH_COLOR, BROWN_PATCH_COLOR]
>>>>>>> 2034002 (Improve grid plot.)
)
GRID_PLOT_CMAP_BOUNDS = [
    EMPTY_CASE - 0.5,
    EMPTY_CASE + 0.5,
    WOLF + 0.5,
<<<<<<< HEAD
    HEALTHY_SHEEP + 0.5,
    GREEN_PATCH + 0.5,
    BROWN_PATCH + 0.5,
    SICK_SHEEP + 0.5,
=======
    SHEEP + 0.5,
    GREEN_PATCH + 0.5,
    BROWN_PATCH + 0.5,
>>>>>>> 2034002 (Improve grid plot.)
]
GRID_PLOT_CMAP_NORM = mpl.colors.BoundaryNorm(
    boundaries=GRID_PLOT_CMAP_BOUNDS, ncolors=GRID_PLOT_CMAP.N
)
<<<<<<< HEAD
<<<<<<< HEAD
GRID_PLOT_CBAR_TICKS = [
    EMPTY_CASE,
    WOLF,
    HEALTHY_SHEEP,
    GREEN_PATCH,
    BROWN_PATCH,
    SICK_SHEEP,
]
=======
>>>>>>> 2034002 (Improve grid plot.)
=======
GRID_PLOT_CBAR_TICKS = [EMPTY_CASE, WOLF, SHEEP, GREEN_PATCH, BROWN_PATCH]
>>>>>>> ec59ebb (Improve comments and add colorbar.)
