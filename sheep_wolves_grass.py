"""Implement a sheep, wolves and grass predation model."""
import mesa
import uuid


class Sheep(mesa.Agent):
    def __init__(self, unique_id, model, energy):
        super.__init__(unique_id, model)
        self.energy = energy
        self.eaten_by_wolf = False

    def step(self):
        self.move()
        self.die()
        self.eat()
        self.reproduce()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -= self.model.config["sheep_move_loss"]

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Patch) and agent.grass:
                agent.grass = False
                self.energy += self.model.config["sheep_gain_from_grass"]
                break

    def reproduce(self):
        random_number = self.random.random()
        if random_number > self.model.config["sheep_reproduction_rate"]:
            new_id = uuid.uuid1()
            new_sheep = Sheep(
                unique_id=new_id.int,
                model=self.model,
                energy=self.model.config["sheep_init_energy"],
            )
            self.model.scheduler.add(new_sheep)
            self.model.grid.place_agent(new_sheep, self.pos)

    def die(self):
        if self.energy < 0 or self.eaten_by_wolf:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)


class Wolf(mesa.Agent):
    def __init__(self, unique_id, model, energy):
        super.__init__(unique_id, model)
        self.energy = energy

    def step(self):
        self.move()
        self.die()
        self.eat()
        self.reproduce()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -= self.model.config["wolf_move_loss"]

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Sheep):
                self.energy += self.model.config["wolf_gain_from_sheep"]
                agent.eaten_by_wolf = True
                agent.die()
                break

    def reproduce(self):
        random_number = self.random.random()
        if random_number > self.model.config["wolf_reproduction_rate"]:
            new_id = uuid.uuid1()
            new_sheep = Wolf(
                unique_id=new_id.int,
                model=self.model,
                energy=self.model.config["wolf_init_energy"],
            )
            self.model.scheduler.add(new_sheep)
            self.model.grid.place_agent(new_sheep, self.pos)

    def die(self):
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.scheduler.remove(self)


class Patch(mesa.Agent):
    def __init__(self, unique_id, model, grass: bool):
        super().__init__(unique_id, model)
        self.grass = grass
        self.count_no_grass = 0

    def step(self):
        if self.count_no_grass > self.model.config["grass_regrowth_time"]:
            self.count_no_grass = 0
            self.green = True

        if not self.grass:
            self.count_no_grass += 1


class PreysPredatorsModel(mesa.Model):
    def __init__(self, config: dict):
        # Model parameters
        self.config = config
        self.grid = mesa.space.MultiGrid(
            self.config["grid_width"], self.config["grid_height"], True
        )
        self.scheduler = mesa.time.SimultaneousActivation(self)
        self.init_all_agents()

    def init_all_agents(self):
        # Fill the grid with grass patches
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                unique_id = uuid.uuid1()
                patch = Patch(grass=True, unique_id=unique_id.int, model=self)
                self.scheduler.add(patch)
                self.grid.place_agent(patch, (i, j))
        # Create and place the sheeps
        for _ in range(self.config.init_nb_sheeps):
            unique_id = uuid.uuid1()
            sheep = Sheep(
                energy=self.config.sheep_init_energy,
                unique_id=unique_id.int,
                model=self,
            )
            self.scheduler.add(sheep)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(sheep, (x, y))
        # Create and place the wolves
        for _ in range(self.config.init_nb_wolves):
            unique_id = uuid.uuid1()
            wolf = Wolf(
                energy=self.config.wolf_init_energy, unique_id=unique_id.int, model=self
            )
            self.scheduler.add(wolf)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(wolf, (x, y))
