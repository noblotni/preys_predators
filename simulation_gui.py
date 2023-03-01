"""GUI to run the simulation."""
import tkinter as tk
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
        )
        self.left_panel.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

    def run(self):
        self.window.mainloop()


class ParametersFrame(tk.Frame):
    def __init__(self, master, width, height, bg):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.create_widgets()

    def create_widgets(self):
        label_sheeps = tk.Label(master=self, text="Initial number of sheeps: ")
        label_sheeps.pack()
        nb_sheeps_scale = tk.Scale(
            master=self,
            from_=cons.MIN_INIT_NB_SHEEPS,
            to_=cons.MAX_INIT_NB_SHEEPS,
            orient=tk.HORIZONTAL,
        )
        nb_sheeps_scale.set(cons.DEFAULT_INIT_NB_SHEEPS)
        nb_sheeps_scale.pack(fill=tk.X)
        label_wolves = tk.Label(master=self, text="Initial number of wolves: ")
        label_wolves.pack()
        nb_wolves_scale = tk.Scale(
            master=self,
            from_=cons.MIN_INIT_NB_WOLVES,
            to_=cons.MAX_INIT_NB_WOLVES,
            orient=tk.HORIZONTAL,
        )
        nb_wolves_scale.set(cons.DEFAULT_INIT_NB_WOLVES)
        nb_wolves_scale.pack(fill=tk.X)
        label_sheeps_reproduction = tk.Label(
            master=self, text="Sheeps' reproduction rate (%):"
        )
        label_sheeps_reproduction.pack()
        sheeps_reproduction_scale = tk.Scale(
            master=self,
            from_=cons.MIN_SHEEP_REPRODUCTION_RATE,
            to_=cons.MAX_SHEEP_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
        )
        sheeps_reproduction_scale.set(cons.DEFAULT_SHEEP_REPRODUCTION_RATE)
        sheeps_reproduction_scale.pack(fill=tk.X)
        label_wolves_reproduction = tk.Label(
            master=self, text="Wolves' reproduction rate (%): "
        )
        label_wolves_reproduction.pack()
        wolves_reproduction_scale = tk.Scale(
            master=self,
            from_=cons.MIN_WOLF_REPRODUCTION_RATE,
            to_=cons.MAX_WOLF_REPRODUCTION_RATE,
            orient=tk.HORIZONTAL,
        )
        wolves_reproduction_scale.pack(fill=tk.X)
        wolves_reproduction_scale.set(cons.DEFAULT_WOLF_REPRODUCTION_RATE)
        label_sheeps_energy = tk.Label(
            master=self, text="Sheeps' energy gain from food:"
        )
        label_sheeps_energy.pack()
        sheeps_energy_gain_scale = tk.Scale(
            master=self,
            from_=cons.MIN_SHEEP_GAIN_FROM_GRASS,
            to_=cons.MAX_SHEEP_GAIN_FROM_GRASS,
            orient=tk.HORIZONTAL,
        )
        sheeps_energy_gain_scale.set(cons.DEFAULT_SHEEP_GAIN_FROM_GRASS)
        sheeps_energy_gain_scale.pack(fill=tk.X)
        label_wolves_energy = tk.Label(
            master=self, text="Wolves' energy gain from food:"
        )
        label_wolves_energy.pack()
        wolves_energy_gain_scale = tk.Scale(
            master=self,
            from_=cons.MIN_WOLF_GAIN_FROM_SHEEP,
            to_=cons.MAX_WOLF_GAIN_FROM_SHEEP,
            orient=tk.HORIZONTAL,
        )
        wolves_energy_gain_scale.set(cons.DEFAULT_WOLF_GAIN_FROM_SHEEP)
        wolves_energy_gain_scale.pack(fill=tk.X)
        setup_button = tk.Button(master=self, text="Set up")
        setup_button.pack()
        run_button = tk.Button(master=self, text="Run")
        run_button.pack()


class PlotsFrame(tk.Frame):
    def __init__(self, master, width, height, bg):
        super().__init__(master=master, width=width, height=height, bg=bg)
        self.create_widgets()

    def dummy_figure(self):
        fig = plt.figure()
        plt.plot([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
        return fig

    def create_widgets(self):
        # Create frames
        frame_up = tk.Frame(master=self, height=self.winfo_height() // 2)
        frame_down = tk.Frame(master=self, height=self.winfo_height() // 2)
        frame_up.pack(expand=True, fill=tk.BOTH)
        frame_down.pack(expand=True, fill=tk.BOTH)
        # Canvas and toolbar to plot the grid
        canvas_grid = FigureCanvasTkAgg(figure=self.dummy_figure(), master=frame_up)
        canvas_grid.draw()
        toolbar_grid = NavigationToolbar2Tk(canvas_grid, frame_up)
        toolbar_grid.update()
        toolbar_grid.pack(fill=tk.X)
        canvas_grid.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        # Canvas and toolbar to plot the evolution of the populations
        canvas_populations = FigureCanvasTkAgg(
            figure=self.dummy_figure(), master=frame_down
        )
        canvas_populations.draw()
        toolbar_populations = NavigationToolbar2Tk(canvas_grid, frame_down)
        toolbar_populations.update()
        toolbar_populations.pack(fill=tk.X)
        canvas_populations.get_tk_widget().pack(expand=True, fill=tk.BOTH)


def main():
    app = SimulationApp()
    app.run()


if __name__ == "__main__":
    main()
