"""Handle the simulation configuration."""
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    grid_width: int = 20
    grid_height: int = 20
    # Number of steps without grass
    # on a patch if eaten by a sheep
    grass_regrowth_time: int = 10
    # Number of sheeps at the first step
    init_nb_sheeps: int = 100
    # Number of sheeps at the first step
    init_nb_wolves: int = 50
    # Initial energy of the sheeps
    sheep_init_energy: int = 20
    # Initial energy of the wolves
    wolf_init_energy: int = 30
    # Energy gained from eating grass
    sheep_gain_from_grass: int = 4
    # Energy gained from eating a sheep
    wolf_gain_from_sheep: int = 20
    # Energy lost by a sheep when moving
    # from a case of the grid to another
    sheep_move_loss: int = 2
    # Energy lost by a wolf when moving
    # from a case to another
    wolf_move_loss: int = 6
    # Probability of reproduction of a sheep
    sheep_reproduction_rate: float = 0.04
    # Probability of reproduction of a wolf
    wolf_reproduction_rate: float = 0.05


# Define default config
DEFAULT_CONFIG = SimulationConfig()
