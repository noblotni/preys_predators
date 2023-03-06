"""GUI to run the simulation."""
import time
from typing import Optional
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sheep_wolves_grass import PreysPredatorsModel, Sheep, Wolf, Patch
import simulation_constants as cons
import simulation_config as config


class SimulationApp:
    """Application to simulate a prey-predator model."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry(
            f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}"
        )
        self.window.title("Preys Predators Simulation")
        self.model_config = create_model_default_config()
        self.model = PreysPredatorsModel(config=self.model_config)
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        """When you click to exit, this function is called"""
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.window.quit()

    def create_widgets(self):
        """Create the widgets of the whole application."""
        self.right_panel = PlotsFrame(
            master=self.window,
            width=3 * self.window.winfo_screenwidth() // 4,
            height=self.window.winfo_screenheight(),
            bg="black",
            app=self,
        )
        self.right_panel.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.left_panel = ParametersFrame(
            master=self.window,
            width=self.window.winfo_screenwidth() // 4,
            height=self.window.winfo_screenheight(),
            bg="black",
            app=self,
        )
        self.left_panel.pack(fill=tk.BOTH, side=tk.RIGHT)

    def run_model(self):
        """Run the prey-predator model."""
        count = 1
        self.model.running = True
        while self.model.running:
            count += 1
            self.model.step()
            population_df = self.model.datacollector.get_model_vars_dataframe()
            population = population_df["population"].to_numpy()
            time_list = [i + 1 for i in range(population.shape[0])]
            nb_sheeps = [pop[0] for pop in population]
            nb_wolves = [pop[1] for pop in population]
            nb_grass_over_four = [pop[2] // 4 for pop in population]
            if self.model_config["add_sickness"]:
                nb_sheeps_sick = [pop[3] for pop in population]
                self.right_panel.update_population_plot(
                    time_list=time_list,
                    nb_sheeps=nb_sheeps,
                    nb_wolves=nb_wolves,
                    nb_grass_over_four=nb_grass_over_four,
                    nb_sheeps_sick=nb_sheeps_sick,
                )
            else:
                self.right_panel.update_population_plot(
                    time_list=time_list,
                    nb_sheeps=nb_sheeps,
                    nb_wolves=nb_wolves,
                    nb_grass_over_four=nb_grass_over_four,
                )
            population_matrix = self.compute_population_matrix()
            self.right_panel.update_grid_plot(population_matrix)
            time.sleep((1 - self.left_panel.model_speed.get() * cons.PERCENT_TO_PROBA))

    def compute_population_matrix(self) -> np.ndarray:
        """Compute the population of the grid."""
            
        healthy_sheeps_matrix = np.zeros((config.GRID_WIDTH, config.GRID_HEIGHT))
        sick_sheeps_matrix = np.zeros_like(healthy_sheeps_matrix)
        wolves_matrix = np.zeros_like(healthy_sheeps_matrix)
        grass_matrix = np.zeros_like(healthy_sheeps_matrix)
        population_matrix = np.zeros_like(healthy_sheeps_matrix)
        # Fill the population matrix
        for cell in self.model.grid.coord_iter():
            cell_content, pos_x, pos_y = cell
            for agent in cell_content:
                if isinstance(agent, Sheep):
                    if self.model_config["add_sickness"] and agent.is_sick:
                        sick_sheeps_matrix[pos_x, pos_y] += 1
                    else:
                        healthy_sheeps_matrix[pos_x, pos_y] += 1
                elif isinstance(agent, Wolf):
                    wolves_matrix[pos_x, pos_y] += 1
                elif isinstance(agent, Patch) and agent.grass:
                    grass_matrix[pos_x, pos_y] += 1
            # Rules for the order of display on the grid plot
            if sick_sheeps_matrix[pos_x, pos_y] and wolves_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.WOLF
            elif healthy_sheeps_matrix[pos_x, pos_y] and wolves_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.WOLF
            elif (
                healthy_sheeps_matrix[pos_x, pos_y] and sick_sheeps_matrix[pos_x, pos_y]
            ):
                population_matrix[pos_x, pos_y] = cons.SICK_SHEEP
            elif healthy_sheeps_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.HEALTHY_SHEEP
            elif sick_sheeps_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.SICK_SHEEP
            elif wolves_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.WOLF
            elif grass_matrix[pos_x, pos_y]:
                population_matrix[pos_x, pos_y] = cons.GREEN_PATCH
            else:
                population_matrix[pos_x, pos_y] = cons.BROWN_PATCH
        return population_matrix

    def run(self):
        """Run the simulation application."""
        self.window.mainloop()


class ParametersFrame(tk.Frame):
    """Frame to set the parameters of the model."""

    def __init__(self, master, width, height, bg, app: SimulationApp):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.app = app
        self.model_speed = tk.IntVar()
        self.init_nb_sheeps = tk.IntVar()
        self.init_nb_wolves = tk.IntVar()
        self.grass_regrowth_time = tk.IntVar()
        self.wolf_reproduction_rate = tk.IntVar()
        self.wolf_gain_from_sheep = tk.IntVar()
        self.sheep_reproduction_rate = tk.IntVar()
        self.sheep_gain_from_grass = tk.IntVar()
        self.sheep_add_sickness = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        """Create all the widgets on the parameters frame."""
        # Canva to display an image
        self.canvas_sheep = tk.Canvas(
            master=self,
            bg="black",
            highlightthickness=0,
            width=self.winfo_reqwidth(),
            height=self.winfo_reqheight() // 3,
        )
        self.canvas_sheep.pack(fill=tk.BOTH, expand=True)
        self.img = Image.open(cons.ASCII_SHEEPS_PATH)
        # Resize image to fit the canvas (To Do)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas_sheep.create_image(
            self.canvas_sheep.winfo_reqwidth() // 2,
            self.canvas_sheep.winfo_reqheight() // 2,
            anchor=tk.CENTER,
            image=self.img,
        )
        self.create_general_settings()
        self.agents_frame = tk.Frame(master=self)
        self.agents_frame.pack(expand=True, fill=tk.BOTH, padx=10)
        self.create_sheeps_settings()
        self.create_wolves_settings()
        self.create_control_buttons()

    def create_general_settings(self):
        """Create the sliders to tweak general parameters."""
        general_settings_frame = tk.Frame(master=self)
        general_settings_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        # Model speed
        model_speed_label = tk.Label(
            master=general_settings_frame, text="Model speed (%)"
        )
        model_speed_label.pack()
        model_speed_scale = tk.Scale(
            master=general_settings_frame,
            from_=cons.MIN_MODEL_SPEED,
            to_=cons.MAX_MODEL_SPEED,
            orient=tk.HORIZONTAL,
            variable=self.model_speed,
        )
        model_speed_scale.pack(fill=tk.X)
        model_speed_scale.set(cons.DEFAULT_MODEL_SPEED)
        # General parameters scales
        label_sheeps = tk.Label(
            master=general_settings_frame, text="Initial number of sheeps: "
        )
        label_sheeps.pack(pady=10)
        nb_sheeps_scale = tk.Scale(
            master=general_settings_frame,
            from_=cons.MIN_INIT_NB_SHEEPS,
            to_=cons.MAX_INIT_NB_SHEEPS,
            orient=tk.HORIZONTAL,
            variable=self.init_nb_sheeps,
        )
        nb_sheeps_scale.set(cons.DEFAULT_INIT_NB_SHEEPS)
        nb_sheeps_scale.pack(fill=tk.X)
        label_wolves = tk.Label(
            master=general_settings_frame, text="Initial number of wolves: "
        )
        label_wolves.pack(pady=10)
        nb_wolves_scale = tk.Scale(
            master=general_settings_frame,
            from_=cons.MIN_INIT_NB_WOLVES,
            to_=cons.MAX_INIT_NB_WOLVES,
            orient=tk.HORIZONTAL,
            variable=self.init_nb_wolves,
        )
        nb_wolves_scale.set(cons.DEFAULT_INIT_NB_WOLVES)
        nb_wolves_scale.pack(fill=tk.X)
        grass_regrowth_label = tk.Label(
            master=general_settings_frame, text="Grass regrowth time (steps):"
        )
        grass_regrowth_label.pack(pady=10)
        grass_regrowth_scale = tk.Scale(
            master=general_settings_frame,
            from_=cons.MIN_GRASS_REGROWTH_TIME,
            to_=cons.MAX_GRASS_REGROWTH_TIME,
            variable=self.grass_regrowth_time,
            orient=tk.HORIZONTAL,
        )
        grass_regrowth_scale.set(cons.DEFAULT_GRASS_REGROWTH_TIME)
        grass_regrowth_scale.pack(fill=tk.X)

    def create_wolves_settings(self):
        """Create the sliders to modify behavior of the wolves."""
        wolves_settings_frame = tk.Frame(master=self.agents_frame)
        wolves_settings_frame.pack(
            expand=True, side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10
        )
        wolves_settings_label = tk.Label(
            master=wolves_settings_frame, text="Wolf settings"
        )
        wolves_settings_label.pack()
        # Slider for the wolf reproduction rate
        label_wolves_reproduction = tk.Label(
            master=wolves_settings_frame, text="Wolves' reproduction rate (%): "
        )
        label_wolves_reproduction.pack(pady=10)
        wolves_reproduction_scale = tk.Scale(
            master=wolves_settings_frame,
            from_=cons.MIN_WOLF_REPRODUCTION_RATE,
            to_=cons.MAX_WOLF_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
            variable=self.wolf_reproduction_rate,
        )
        wolves_reproduction_scale.pack(fill=tk.X)
        wolves_reproduction_scale.set(cons.DEFAULT_WOLF_REPRODUCTION_RATE)

        # Slider for the energy gain of the wolves when they
        # eat sheeps
        label_wolves_energy = tk.Label(
            master=wolves_settings_frame, text="Wolves' energy gain from food:"
        )
        label_wolves_energy.pack(pady=10)
        wolves_energy_gain_scale = tk.Scale(
            master=wolves_settings_frame,
            from_=cons.MIN_WOLF_GAIN_FROM_SHEEP,
            to_=cons.MAX_WOLF_GAIN_FROM_SHEEP,
            orient=tk.HORIZONTAL,
            variable=self.wolf_gain_from_sheep,
        )
        wolves_energy_gain_scale.set(cons.DEFAULT_WOLF_GAIN_FROM_SHEEP)
        wolves_energy_gain_scale.pack(fill=tk.X)

    def create_sheeps_settings(self):
        """Create the widgets to change the sheeps behavior."""
        sheeps_settings_frame = tk.Frame(master=self.agents_frame)
        sheeps_settings_frame.pack(
            expand=True, side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10
        )
        sheeps_settings_label = tk.Label(
            master=sheeps_settings_frame, text="Sheep settings"
        )
        sheeps_settings_label.pack()

        # Slider for the sheep reproduction rate
        label_sheeps_reproduction = tk.Label(
            master=sheeps_settings_frame, text="Sheeps' reproduction rate (%):"
        )
        label_sheeps_reproduction.pack(pady=10)
        sheeps_reproduction_scale = tk.Scale(
            master=sheeps_settings_frame,
            from_=cons.MIN_SHEEP_REPRODUCTION_RATE,
            to_=cons.MAX_SHEEP_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
            variable=self.sheep_reproduction_rate,
        )
        sheeps_reproduction_scale.set(cons.DEFAULT_SHEEP_REPRODUCTION_RATE)
        sheeps_reproduction_scale.pack(fill=tk.X)

        # Slider for the sheep energy gain when it eats grass
        label_sheeps_energy = tk.Label(
            master=sheeps_settings_frame, text="Sheeps' energy gain from food:"
        )
        label_sheeps_energy.pack(pady=10)
        sheeps_energy_gain_scale = tk.Scale(
            master=sheeps_settings_frame,
            from_=cons.MIN_SHEEP_GAIN_FROM_GRASS,
            to_=cons.MAX_SHEEP_GAIN_FROM_GRASS,
            orient=tk.HORIZONTAL,
            variable=self.sheep_gain_from_grass,
        )
        sheeps_energy_gain_scale.set(cons.DEFAULT_SHEEP_GAIN_FROM_GRASS)
        sheeps_energy_gain_scale.pack(fill=tk.X)

        # Checkbox to add a disease among the sheeps
        add_sickness_checkbox = tk.Checkbutton(
            master=sheeps_settings_frame,
            text="Add a sickness among the sheeps",
            variable=self.sheep_add_sickness,
        )
        if cons.DEFAULT_ADD_SICKNESS:
            add_sickness_checkbox.select()
        add_sickness_checkbox.pack(fill=tk.X, pady=10)

    def create_control_buttons(self):
        """Create all the control buttons of the parameters frame."""
        button_frame = tk.Frame(master=self, bg="black")
        button_frame.pack(pady=10, padx=10)
        setup_button = tk.Button(
            master=button_frame, text="Set up", command=self.setup_model
        )
        setup_button.pack(side=tk.LEFT, padx=10)
        stop_button = tk.Button(
            master=button_frame, text="Stop", command=self.stop_model
        )
        stop_button.pack(side=tk.LEFT, padx=10)
        run_button = tk.Button(master=button_frame, text="Run", command=self.run_model)
        run_button.pack(side=tk.LEFT, padx=10)

    def setup_model(self):
        """Set the values of the model parameters."""
        self.app.model.running = False
        self.app.model_config["init_nb_sheeps"] = self.init_nb_sheeps.get()
        self.app.model_config["init_nb_wolves"] = self.init_nb_wolves.get()
        self.app.model_config["grass_regrowth_time"] = self.grass_regrowth_time.get()
        self.app.model_config["sheep_reproduction_rate"] = (
            self.sheep_reproduction_rate.get() * cons.PERCENT_TO_PROBA
        )
        self.app.model_config["wolf_reproduction_rate"] = (
            self.wolf_reproduction_rate.get() * cons.PERCENT_TO_PROBA
        )
        self.app.model_config[
            "sheep_gain_from_grass"
        ] = self.sheep_gain_from_grass.get()
        self.app.model_config["wolf_gain_from_sheep"] = self.wolf_gain_from_sheep.get()
        self.app.model_config["add_sickness"] = self.sheep_add_sickness.get() > 0
        self.app.model = PreysPredatorsModel(self.app.model_config)

    def stop_model(self):
        """Stop the model."""
        self.app.model.running = False

    def run_model(self):
        """Start the model.

        The model runs in a different thread so that the
        user can still change settings on the GUI.
        """
        thread = Thread(target=self.app.run_model)
        thread.start()


class PlotsFrame(tk.Frame):
    """Frame where to put plots."""

    def __init__(self, master, width: int, height: int, bg: int, app: SimulationApp):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.app = app
        self.init_grid_plot()
        self.init_population_plot()
        self.create_widgets()

    def init_population_plot(self):
        """Initialize the population plot (at the bottom right of the GUI)."""
        self.population_figure = plt.figure()
        self.pop_ax = self.population_figure.add_subplot()
        self.pop_ax.plot(
            [], [], label="Total number of sheeps", color="blue", linewidth=4
        )
        self.pop_ax.plot([], [], label="Number of wolves", color="red", linewidth=4)
        self.pop_ax.plot([], [], label="Grass / 4", color="green", linewidth=4)
        if self.app.model_config["add_sickness"]:
            self.pop_ax.plot(
                [], [], label="NUmber of sick sheeps", color="black", linewidth=4
            )
        self.pop_ax.set_xlabel("Time (Number of steps)")
        self.pop_ax.set_ylabel("Population")
        self.pop_ax.grid()
        self.pop_ax.legend()

    def update_population_plot(
        self,
        time_list: list,
        nb_sheeps: list,
        nb_wolves: list,
        nb_grass_over_four: list,
        nb_sheeps_sick: Optional[list] = None,
    ):
        """Update the population plot with the latest data."""
        self.pop_ax.clear()
        self.pop_ax.plot(
            time_list,
            nb_sheeps,
            label="Total number of sheeps",
            color="blue",
            linewidth=4,
        )
        self.pop_ax.fill_between(time_list, nb_sheeps, 0, color="blue", alpha=0.3)
        self.pop_ax.plot(
            time_list, nb_wolves, label="Number of wolves", color="red", linewidth=4
        )
        self.pop_ax.fill_between(time_list, nb_wolves, 0, color="red", alpha=0.3)
        self.pop_ax.plot(
            time_list, nb_grass_over_four, label="Grass /4", color="green", linewidth=4
        )
        self.pop_ax.fill_between(
            time_list, nb_grass_over_four, 0, color="green", alpha=0.3
        )
        if nb_sheeps_sick:
            self.pop_ax.plot(time_list, nb_sheeps_sick, color="black", linewidth=4)
            self.pop_ax.fill_between(
                time_list, nb_sheeps_sick, 0, color="black", alpha=0.3
            )
        self.pop_ax.fill_between(time, nb_grass_over_four, 0, color="green", alpha=0.3)
        self.pop_ax.set_xlabel("Time (number of steps)")
        self.pop_ax.set_ylabel("Population")
        self.pop_ax.grid()
        self.pop_ax.legend()
        self.canvas_populations.draw()

    def init_grid_plot(self):
        """Initialize the grid plot."""
        self.grid_figure, self.gridfig_ax = plt.subplots(1)
        # PLot an empty grid
        self.gridfig_ax.matshow(
            config.EMPTY_GRID,
            cmap=cons.GRID_PLOT_CMAP,
            norm=cons.GRID_PLOT_CMAP_NORM,
        )
        self.gridfig_ax.set_title("Current state of the grid")
        self.gridfig_ax.axis("off")
        cbar = self.grid_figure.colorbar(
            mpl.cm.ScalarMappable(
                cmap=cons.GRID_PLOT_CMAP, norm=cons.GRID_PLOT_CMAP_NORM
            ),
            ax=self.gridfig_ax,
            ticks=cons.GRID_PLOT_CBAR_TICKS,
        )
        cbar.ax.set_yticklabels(
            ["Empty", "Wolf", "Healthy sheep", "Grass", "Dirt", "Sick sheep"]
        )

    def update_grid_plot(self, population_matrix: np.ndarray):
        """Update the grid plot with the latest data."""
        self.gridfig_ax.clear()
        self.gridfig_ax.matshow(
            population_matrix, cmap=cons.GRID_PLOT_CMAP, norm=cons.GRID_PLOT_CMAP_NORM
        )
        self.gridfig_ax.set_title("Current state of the grid")
        self.gridfig_ax.axis("off")
        self.canvas_grid.draw()

    def create_widgets(self):
        """Create the widgets on the plot panel."""
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


def create_model_default_config() -> dict:
    """Create the default configuration of the model.

    Returns:
        model_config (dict): a dictionary containing all the default values of
            the model parameters.
    """
    model_config = {}
    model_config["init_nb_sheeps"] = cons.DEFAULT_INIT_NB_SHEEPS
    model_config["init_nb_wolves"] = cons.DEFAULT_INIT_NB_WOLVES
    model_config["grass_regrowth_time"] = cons.DEFAULT_GRASS_REGROWTH_TIME
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
    # add the sickness config.
    model_config["add_sickness"] = config.ADD_SICKNESS
    model_config["sickness_severity"] = config.SICKNESS_SEVERITY
    model_config["proba_sickness_transmission"] = config.PROBA_SICKNESS_TRANSMISSION
    model_config["sheep_sanity_proba"] = config.SHEEP_SANITY_PROBA
    model_config["sheep_cure_proba"] = config.SHEEP_CURE_PROBA
    return model_config


def main():
    """Entry point of the simulation program."""
    app = SimulationApp()
    app.run()


if __name__ == "__main__":
    main()
