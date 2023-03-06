"""Handle the simulation configuration."""
import os
import numpy as np

GRID_WIDTH = int(os.environ.get("GRID_WIDTH", default=40))
GRID_HEIGHT = int(os.environ.get("GRID_HEIGHT", default=65))
# Number of steps without grass
# on a patch if eaten by a sheep
GRASS_REGROWTH_TIME = int(os.environ.get("GRASS_REGROWTH_TIME", default=30))
# Initial energy of the sheeps
SHEEP_INIT_ENERGY = int(os.environ.get("SHEEP_INIT_ENERGY", default=10))
# Initial energy of the wolves
WOLF_INIT_ENERGY = int(os.environ.get("WOLF_INIT_ENERGY", default=10))
# Energy lost by a sheep when moving
# from a case of the grid to another
SHEEP_MOVE_LOSS = int(os.environ.get("SHEEP_MOVE_LOSS", default=1))
# Energy lost by a wolf when moving
# from a case to another
WOLF_MOVE_LOSS = int(os.environ.get("WOLF_MOVE_LOSS", default=1))


# GUI
EMPTY_GRID = np.zeros((GRID_WIDTH, GRID_HEIGHT))
