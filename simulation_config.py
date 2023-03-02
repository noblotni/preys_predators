"""Handle the simulation configuration."""
import os

GRID_WIDTH = int(os.environ.get("GRID_WIDTH", default=50))
GRID_HEIGHT = int(os.environ.get("GRID_HEIGHT", default=50))
# Number of steps without grass
# on a patch if eaten by a sheep
GRASS_REGROWTH_TIME = int(os.environ.get("GRASS_REGROWTH_TIME", default=10))
# Initial energy of the sheeps
SHEEP_INIT_ENERGY = int(os.environ.get("SHEEP_INIT_ENERGY", default=20))
# Initial energy of the wolves
WOLF_INIT_ENERGY = int(os.environ.get("WOLF_INIT_ENERGY", default=30))
# Energy lost by a sheep when moving
# from a case of the grid to another
SHEEP_MOVE_LOSS = int(os.environ.get("SHEEP_MOVE_LOSS", default=2))
# Energy lost by a wolf when moving
# from a case to another
WOLF_MOVE_LOSS = int(os.environ.get("WOLF_MOVE_LOSS", default=3))
