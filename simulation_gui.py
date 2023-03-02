"""GUI to run the simulation."""
import tkinter as tk
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from sheep_wolves_grass import PreysPredatorsModel
import simulation_constants as cons
import simulation_config as config


class SimulationApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1000x800")
        self.window.title("Preys Predators Simulation")
        self.model_config = create_model_default_config()
        self.model = PreysPredatorsModel(config=self.model_config)
        self.create_widgets()

    def create_widgets(self):
        self.right_panel = PlotsFrame(
            master=self.window,
            width=3 * self.window.winfo_width() // 4,
            height=self.window.winfo_height(),
            bg="black",
        )
        self.right_panel.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        self.left_panel = ParametersFrame(
            master=self.window,
            width=self.window.winfo_width() // 4,
            height=self.window.winfo_height(),
            bg="gray",
            app=self,
        )
        self.left_panel.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

    def run_model(self):
        count = 1
        self.model.running = True
        while self.model.running:
            count += 1
            self.model.step()
            population_df = self.model.datacollector.get_model_vars_dataframe()
            population = population_df["population"].to_numpy()
            time = [i + 1 for i in range(population.shape[0])]
            nb_sheeps = [pop[0] for pop in population]
            nb_wolves = [pop[1] for pop in population]
            self.right_panel.update_population_plot(
                time=time, nb_sheeps=nb_sheeps, nb_wolves=nb_wolves
            )

    def run(self):
        self.window.mainloop()


class ParametersFrame(tk.Frame):
    def __init__(self, master, width, height, bg, app: SimulationApp):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        label_sheeps = tk.Label(master=self, text="Initial number of sheeps: ")
        label_sheeps.pack()
        self.init_nb_sheeps = tk.IntVar()
        nb_sheeps_scale = tk.Scale(
            master=self,
            from_=cons.MIN_INIT_NB_SHEEPS,
            to_=cons.MAX_INIT_NB_SHEEPS,
            orient=tk.HORIZONTAL,
            variable=self.init_nb_sheeps,
        )
        nb_sheeps_scale.set(cons.DEFAULT_INIT_NB_SHEEPS)
        nb_sheeps_scale.pack(fill=tk.X)
        label_wolves = tk.Label(master=self, text="Initial number of wolves: ")
        label_wolves.pack()
        self.init_nb_wolves = tk.IntVar()
        nb_wolves_scale = tk.Scale(
            master=self,
            from_=cons.MIN_INIT_NB_WOLVES,
            to_=cons.MAX_INIT_NB_WOLVES,
            orient=tk.HORIZONTAL,
            variable=self.init_nb_wolves,
        )
        nb_wolves_scale.set(cons.DEFAULT_INIT_NB_WOLVES)
        nb_wolves_scale.pack(fill=tk.X)
        label_sheeps_reproduction = tk.Label(
            master=self, text="Sheeps' reproduction rate (%):"
        )
        label_sheeps_reproduction.pack()
        self.sheep_reproduction_rate = tk.IntVar()
        sheeps_reproduction_scale = tk.Scale(
            master=self,
            from_=cons.MIN_SHEEP_REPRODUCTION_RATE,
            to_=cons.MAX_SHEEP_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
            variable=self.sheep_reproduction_rate,
        )
        sheeps_reproduction_scale.set(cons.DEFAULT_SHEEP_REPRODUCTION_RATE)
        sheeps_reproduction_scale.pack(fill=tk.X)
        label_wolves_reproduction = tk.Label(
            master=self, text="Wolves' reproduction rate (%): "
        )
        label_wolves_reproduction.pack()
        self.wolf_reproduction_rate = tk.IntVar()
        wolves_reproduction_scale = tk.Scale(
            master=self,
            from_=cons.MIN_WOLF_REPRODUCTION_RATE,
            to_=cons.MAX_WOLF_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
            variable=self.wolf_reproduction_rate,
        )
        wolves_reproduction_scale.pack(fill=tk.X)
        wolves_reproduction_scale.set(cons.DEFAULT_WOLF_REPRODUCTION_RATE)
        label_sheeps_energy = tk.Label(
            master=self, text="Sheeps' energy gain from food:"
        )
        label_sheeps_energy.pack()
        self.sheep_gain_from_grass = tk.IntVar()
        sheeps_energy_gain_scale = tk.Scale(
            master=self,
            from_=cons.MIN_SHEEP_GAIN_FROM_GRASS,
            to_=cons.MAX_SHEEP_GAIN_FROM_GRASS,
            orient=tk.HORIZONTAL,
            variable=self.sheep_gain_from_grass,
        )
        sheeps_energy_gain_scale.set(cons.DEFAULT_SHEEP_GAIN_FROM_GRASS)
        sheeps_energy_gain_scale.pack(fill=tk.X)
        label_wolves_energy = tk.Label(
            master=self, text="Wolves' energy gain from food:"
        )
        label_wolves_energy.pack()
        self.wolf_gain_from_sheep = tk.IntVar()
        wolves_energy_gain_scale = tk.Scale(
            master=self,
            from_=cons.MIN_WOLF_GAIN_FROM_SHEEP,
            to_=cons.MAX_WOLF_GAIN_FROM_SHEEP,
            orient=tk.HORIZONTAL,
            variable=self.wolf_gain_from_sheep,
        )
        wolves_energy_gain_scale.set(cons.DEFAULT_WOLF_GAIN_FROM_SHEEP)
        wolves_energy_gain_scale.pack(fill=tk.X)
        setup_button = tk.Button(master=self, text="Set up", command=self.setup_model)
        setup_button.pack()
        run_button = tk.Button(master=self, text="Run", command=self.run_model)
        run_button.pack()

    def setup_model(self):
        self.app.model.running = False
        self.app.model_config["init_nb_sheeps"] = self.init_nb_sheeps.get()
        self.app.model_config["init_nb_wolves"] = self.init_nb_wolves.get()
        self.app.model_config["sheep_reproduction_rate"] = (
            self.sheep_reproduction_rate.get() * cons.PERCENT_TO_PROBA
        )
        self.app.model_config["wolf_reproducyion_rate"] = (
            self.wolf_reproduction_rate.get() * cons.PERCENT_TO_PROBA
        )
        self.app.model_config[
            "sheep_gain_from_grass"
        ] = self.sheep_gain_from_grass.get()
        self.app.model_config["wolf_gain_from_sheep"] = self.wolf_gain_from_sheep.get()
        self.app.model = PreysPredatorsModel(self.app.model_config)

    def run_model(self):
        thread = Thread(target=self.app.run_model)
        thread.start()


class PlotsFrame(tk.Frame):
    def __init__(self, master, width, height, bg):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.init_grid_plot()
        self.init_population_plot()
        self.create_widgets()

    def init_population_plot(self):
        self.population_figure = plt.figure()
        self.pop_ax = self.population_figure.add_subplot()
        self.pop_ax.plot([], [], label="Number of sheeps", color="blue")
        self.pop_ax.plot([], [], label="Number of wolves", color="red")
        self.pop_ax.grid()
        self.pop_ax.legend()

    def update_population_plot(self, time, nb_sheeps, nb_wolves):
        self.pop_ax.clear()
        self.pop_ax.plot(time, nb_sheeps, label="Number of sheeps", color="blue")
        self.pop_ax.plot(time, nb_wolves, label="Number of wolves", color="red")
        self.pop_ax.grid()
        self.pop_ax.legend()
        self.canvas_populations.draw()

    def init_grid_plot(self):
        self.grid_figure = plt.figure()
        self.grid_ax = self.grid_figure.add_subplot()
        self.grid_ax.grid()

    def create_widgets(self):
        # Create frames
        frame_up = tk.Frame(master=self, height=self.winfo_height() // 2)
        frame_down = tk.Frame(master=self, height=self.winfo_height() // 2)
        frame_up.pack(expand=True, fill=tk.BOTH)
        frame_down.pack(expand=True, fill=tk.BOTH)
        # Canvas and toolbar to plot the grid
        self.canvas_grid = FigureCanvasTkAgg(figure=self.grid_figure, master=frame_up)
        self.canvas_grid.draw()
        toolbar_grid = NavigationToolbar2Tk(self.canvas_grid, frame_up)
        toolbar_grid.update()
        toolbar_grid.pack(fill=tk.X)
        self.canvas_grid.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        # Canvas and toolbar to plot the evolution of the populations
        self.canvas_populations = FigureCanvasTkAgg(
            figure=self.population_figure, master=frame_down
        )
        self.canvas_populations.draw()
        toolbar_populations = NavigationToolbar2Tk(self.canvas_populations, frame_down)
        toolbar_populations.update()
        toolbar_populations.pack(fill=tk.X)
        self.canvas_populations.get_tk_widget().pack(expand=True, fill=tk.BOTH)


def create_model_default_config():
    model_config = {}
    model_config["init_nb_sheeps"] = cons.DEFAULT_INIT_NB_SHEEPS
    model_config["init_nb_wolves"] = cons.DEFAULT_INIT_NB_WOLVES
    model_config["grass_regrowth_time"] = config.GRASS_REGROWTH_TIME
    model_config["grid_width"] = config.GRID_WIDTH
    model_config["grid_height"] = config.GRID_HEIGHT
    model_config["sheep_reproduction_rate"] = (
        cons.DEFAULT_SHEEP_REPRODUCTION_RATE * cons.PERCENT_TO_PROBA
    )
    model_config["wolf_reproduction_rate"] = (
        cons.DEFAULT_WOLF_REPRODUCTION_RATE * cons.PERCENT_TO_PROBA
    )
    model_config["sheep_gain_from_grass"] = cons.DEFAULT_SHEEP_GAIN_FROM_GRASS
    model_config["wolf_gain_from_sheep"] = cons.DEFAULT_WOLF_GAIN_FROM_SHEEP
    model_config["sheep_init_energy"] = config.SHEEP_INIT_ENERGY
    model_config["wolf_init_energy"] = config.WOLF_INIT_ENERGY
    model_config["sheep_move_loss"] = config.SHEEP_MOVE_LOSS
    model_config["wolf_move_loss"] = config.WOLF_MOVE_LOSS
    return model_config


def main():
    app = SimulationApp()
    app.run()


if __name__ == "__main__":
    main()
