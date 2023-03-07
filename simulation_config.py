"""Handle the simulation configuration."""
import os
import numpy as np

GRID_WIDTH = int(os.environ.get("GRID_WIDTH", default=40))
GRID_HEIGHT = int(os.environ.get("GRID_HEIGHT", default=65))
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
# SICKNESS
# add a sickness that is able to propagate among Sheep agents
ADD_SICKNESS = os.environ.get("ADD_SICKNESS", default=True)
# control the probability to die when infected by the above sickness
SICKNESS_SEVERITY = float(os.environ.get("SICKNESS_SEVERITY", default=0.2))
# control the probability of being infected by the illness when sharing a cell with an infected agent
PROBA_SICKNESS_TRANSMISSION = float(
    os.environ.get("PROBA_SICKNESS_TRANSMISSION", default=0.7)
)
# control the probability of popping sane for sheeps (as opposed to popping already infected)
SHEEP_SANITY_PROBA = float(os.environ.get("SHEEP_SANITY_PROBA", default=0.50))
# control the probability for infected sheeps to recover from illness at each step
SHEEP_CURE_PROBA = float(os.environ.get("SHEEP_CURE_PROBA", default=0.20))
