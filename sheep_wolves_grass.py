"""Implement a sheep, wolves and grass predation model."""
import logging
import mesa
import uuid

from custom_errors import UnsupportedMovingMethodError

# pylint: disable=consider-using-f-string, line-too-long, logging-format-interpolation, logging-too-many-args

logging.basicConfig(level=logging.INFO)


class Sheep(mesa.Agent):
    """Handle sheep agents."""

    def __init__(
        self,
        unique_id,
        model,
        energy,
        way_to_move: str = "random",
    ):
        super().__init__(unique_id, model)
        # note: unique_id and model attributes inherit from the Agent class
        self.energy = energy
        self.eaten_by_wolf = False
        # controls the Sheep agent's way to move on the grid (Random Walker by default)
        self.way_to_move = way_to_move
        self.is_sick = self.random.random() > self.model.config["sheep_sanity_proba"]
        logging.info(
            "[Sheep] Creating a ship agent with ID {}, energy = {} and is_sick = {}".format(
                unique_id, energy, self.is_sick
            )
        )

    def step(self):
        """Generic step for a sheep."""
        if not self in self.model.died_agents:
            # this order matters: see the doc
            self.move()
            if self.model.config["add_sickness"]:
                self.update_sickness()
            # note: die() method does not mean the current agent will die at this step
            self.die()
            self.eat()
            self.reproduce()

    def move(self):
        """When a sheep moves on the grid."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if self.way_to_move == "random":
            # pick a new position at random
            new_position = self.random.choice(possible_steps)
        else:
            raise UnsupportedMovingMethodError

        self.model.grid.move_agent(self, new_position)
        # when a sheep moves, it looses an energy unit
        self.energy -= self.model.config["sheep_move_loss"]
        logging.debug(
            "[Sheep] Sheep agent with ID {} has remaining energy of {}".format(
                self.unique_id, self.energy
            )
        )

    def eat(self):
        """When a sheep eats grass."""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Patch) and agent.grass:
                # a surrounding Patch agent has grass to provide
                agent.grass = False
                # the Sheep agent eats the grass and gains energy
                self.energy += self.model.config["sheep_gain_from_grass"]
                logging.info(
                    "[Sheep] Sheep agent with ID {} eats a Grass patch. Remaining energy is {}".format(
                        self.unique_id, self.energy
                    )
                )
                break

    def reproduce(self):
        """When sheeps breed."""
        random_number = self.random.random()
        if random_number < self.model.config["sheep_reproduction_rate"]:
            new_id = uuid.uuid1()
            new_sheep = Sheep(
                unique_id=new_id.int,
                model=self.model,
                energy=self.model.config["sheep_init_energy"],
            )
            new_sheep.pos = self.pos
            # note: we could also make the new sheep pop on a surrounding grid cell
            self.model.born_agents.append(new_sheep)

    def die(self):
        """When a sheep dies either from being eaten by a wolf or by natural death."""
        if (
            self.energy < 0 or self.eaten_by_wolf
        ) and not self in self.model.died_agents:
            self.model.died_agents.append(self)
            logging.info(
                "[Sheep] Sheep agent with ID {} has died.".format(self.unique_id)
            )
        if self.model.config["add_sickness"]:
            if not self in self.model.died_agents and self.is_sick:
                dies_from_sickness = (
                    self.random.random() < self.model.config["sickness_severity"]
                )
                if dies_from_sickness:
                    self.model.died_agents.append(self)
                    logging.info(
                        "[Sheep] Sheep agent with ID {} has died from sickness.".format(
                            self.unique_id
                        )
                    )

    def update_sickness(self):
        """Method used to determine if the agent gets infected by sickness at this step."""
        if self.is_sick:
            heal_from_sickness = (1 - self.random.random()) > self.model.config[
                "sheep_cure_proba"
            ]
            if heal_from_sickness:
                self.is_sick = False
        if not self.is_sick:
            number_surrounding_agents_infected = 0
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for agent in cellmates:
                if isinstance(agent, Sheep) and agent.is_sick:
                    number_surrounding_agents_infected += 1
            get_sickness = (
                self.random.random()
                > number_surrounding_agents_infected
                * self.model.config["proba_sickness_transmission"]
            )
            self.is_sick = get_sickness


class Wolf(mesa.Agent):
    """Handle wolves agents."""

    def __init__(self, unique_id, model, energy, way_to_move: str = "random"):
        super().__init__(unique_id, model)
        self.energy = energy
        logging.info(
            "[Wolf] Creating a wolf agent with ID {} and energy = {}".format(
                unique_id, energy
            )
        )
        self.way_to_move = way_to_move

    def step(self):
        """Generic step for wolf agents."""
        if not self in self.model.died_agents:
            # this order matters: see the doc
            self.move()
            self.die()
            self.eat()
            self.reproduce()

    def move(self):
        """When a wolf moves on the grid."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if self.way_to_move == "random":
            # pick a new position at random
            new_position = self.random.choice(possible_steps)
        else:
            raise UnsupportedMovingMethodError

        self.model.grid.move_agent(self, new_position)
        self.energy -= self.model.config["wolf_move_loss"]

    def eat(self):
        """When a wolf eats a sheep."""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Sheep) and not agent in self.model.died_agents:
                self.energy += self.model.config["wolf_gain_from_sheep"]
                logging.info(
                    "[Wolf] Wolf agent with ID {} has eaten Sheep agent with ID {}.".format(
                        self.unique_id, agent.unique_id
                    )
                )
                agent.eaten_by_wolf = True
                agent.die()
                break

    def reproduce(self):
        """When wolves breed."""
        random_number = self.random.random()
        if random_number < self.model.config["wolf_reproduction_rate"]:
            new_id = uuid.uuid1()
            new_wolf = Wolf(
                unique_id=new_id.int,
                model=self.model,
                energy=self.model.config["wolf_init_energy"],
            )
            new_wolf.pos = self.pos
            self.model.born_agents.append(new_wolf)

    def die(self):
        """When a wolf dies of natural death."""
        if self.energy < 0 and not self in self.model.died_agents:
            self.model.died_agents.append(self)
            logging.info(
                "[Wolf] Wolf agent with ID {} has died.".format(self.unique_id)
            )


class Patch(mesa.Agent):
    """Handle the grass."""

    def __init__(self, unique_id, model, grass: bool):
        super().__init__(unique_id, model)
        # the grass attribute is True if the current Patch agent has grass to offer sheeps
        self.grass = grass
        # the count_no_grass attributes is used for grass regeneration
        self.count_no_grass = 0

    def step(self):
        """Handle a generic step for grass agents."""
        if self.count_no_grass > self.model.config["grass_regrowth_time"]:
            self.count_no_grass = 0
            self.grass = True

        if not self.grass:
            self.count_no_grass += 1


class Shepherd(mesa.Agent):
    """
    Create a special agent (unique): the shepherd.
    The shepherd has got 2 powers:
        - he/she protects the sheeps surrounding him/her (Moore) from being eaten by wolves
        - he/she has the ability to kill a wolf surrounding him/her
    The Shepherd is a Random Walker on the grid.
    """

    #
    #
    # Not used thereafter.
    #
    #

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        logging.info(
            "[Shepherd] Creating a shepherd agent with ID {}".format(unique_id)
        )

    def step(self):
        """Generic step for the Shepherd agent."""
        if not self in self.model.died_agents:
            # this order matters: see the doc
            self.move()
            self.kill_wolf()

    def move(self):
        """When the shepherd moves on the grid."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.protect_surrounding_sheeps()

    def protect_surrounding_sheeps(self):
        """Handle the protection of the shepherd on surrounding sheeps."""
        # unprotect all Sheep agents
        for agent in self.model.scheduler.agents:
            if isinstance(agent, Sheep) and agent.protected_by_shepherd:
                agent.protected_by_shepherd = False
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Sheep):
                agent.protected_by_shepherd = True

    def kill_wolf(self):
        """When the shepherd tries to kill a surrounding wolf."""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Wolf):
                logging.info(
                    "[Shepherd] Shepherd agent with ID {} has killed Wolf agent with ID {}.".format(
                        self.unique_id, agent.unique_id
                    )
                )
                agent.killed_by_shepherd = True
                agent.die()
                break


class PreysPredatorsModel(mesa.Model):
    """Base class for the Preys-Predators model."""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.grid = mesa.space.MultiGrid(
            self.config["grid_width"], self.config["grid_height"], True
        )
        self.scheduler = mesa.time.RandomActivation(self)
        self.datacollector = mesa.DataCollector(
            model_reporters={"population": compute_population}
        )
        self.running = False
        self.died_agents = []
        self.born_agents = []
        self.init_all_agents()
        print("[Model] Created a new Preys-Predators model successfully.")
        print("[Model] Sickness added: ", str(self.config["add_sickness"]))
        print("[Model] Sickness severity: ", str(self.config["sickness_severity"]))
        print(
            "[Model] Probability of transmitting the sickness: ",
            str(self.config["proba_sickness_transmission"]),
        )
        print(
            "[Model] Probability for sheeps of being born sane: ",
            str(self.config["sheep_sanity_proba"]),
        )
        print(
            "[Model] Probability of healing from sickness: ",
            str(self.config["sheep_cure_proba"]),
        )

    def init_all_agents(self):
        """Create the initial population."""
        # Fill the grid with grass patches
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                unique_id = uuid.uuid1()
                patch = Patch(grass=True, unique_id=unique_id.int, model=self)
                self.scheduler.add(patch)
                self.grid.place_agent(patch, (i, j))
        # Create and place the sheeps
        for _ in range(self.config["init_nb_sheeps"]):
            unique_id = uuid.uuid1()
            sheep = Sheep(
                energy=self.config["sheep_init_energy"],
                unique_id=unique_id.int,
                model=self,
            )
            self.scheduler.add(sheep)
            sheep_x_coord = self.random.randrange(self.grid.width)
            sheep_y_coord = self.random.randrange(self.grid.height)
            self.grid.place_agent(sheep, (sheep_x_coord, sheep_y_coord))
        # Create and place the wolves
        for _ in range(self.config["init_nb_wolves"]):
            unique_id = uuid.uuid1()
            wolf = Wolf(
                energy=self.config["wolf_init_energy"],
                unique_id=unique_id.int,
                model=self,
            )
            self.scheduler.add(wolf)
            wolf_x_coord = self.random.randrange(self.grid.width)
            wolf_y_coord = self.random.randrange(self.grid.height)
            self.grid.place_agent(wolf, (wolf_x_coord, wolf_y_coord))

    def kill_agents(self):
        """Handle the death of agents."""
        while self.died_agents:
            agent = self.died_agents.pop()
            self.scheduler.remove(agent)
            self.grid.remove_agent(agent)

    def give_birth_to_agents(self):
        """Create new agents (reproduction)."""
        while self.born_agents:
            agent = self.born_agents.pop()
            self.scheduler.add(agent)
            self.grid.place_agent(agent, agent.pos)

    def step(self):
        """Handle a generic step for the whole model."""
        self.datacollector.collect(self)
        self.scheduler.step()
        self.kill_agents()
        self.give_birth_to_agents()


def compute_population(model: PreysPredatorsModel):
    """Count the number of sheeps, wolves and grass on the grid."""
    count_sheeps = 0
    count_wolves = 0
    count_grass = 0
    count_sick = 0
    for agent in model.scheduler.agents:
        if isinstance(agent, Sheep):
            count_sheeps += 1
            if agent.is_sick:
                count_sick += 1
        elif isinstance(agent, Wolf):
            count_wolves += 1
        elif isinstance(agent, Patch) and agent.grass:
            count_grass += 1
    return (count_sheeps, count_wolves, count_grass, count_sick)
