"""Line plot multiple pd.DataFrame results from simulation"""

from pathlib import Path
from typing import Literal, Optional

import matplotlib.figure as fig
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.axes import Axes

from .globals_types import numpy_flt

# type aliases
Scale = Literal["linear", "log"]

# size of figures to display. set size to match screen monitor size
FIG_SIZE: tuple[float, float] = (16, 8)


def oscilloscope_colors() -> None:
    """Set style properties to look like dark oscilloscope screen"""

    plt.rcParams["lines.color"] = "#d8b200"
    plt.rcParams["patch.edgecolor"] = "#d8b200"

    plt.rcParams["text.color"] = "#d8b200"

    plt.rcParams["axes.facecolor"] = "black"
    plt.rcParams["axes.edgecolor"] = "#d8b200"
    plt.rcParams["axes.labelcolor"] = "#d8b200"

    plt.rcParams["axes.prop_cycle"] = cycler(
        color=["#00FF00", "#00ffff", "#ff00ff", "#ffd200"]
    )

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.grid.axis"] = "both"
    plt.rcParams["grid.linestyle"] = "dotted"
    plt.rcParams["xtick.minor.visible"] = True
    plt.rcParams["ytick.minor.visible"] = True

    plt.rcParams["xtick.color"] = "#d8b200"
    plt.rcParams["ytick.color"] = "#d8b200"

    plt.rcParams["grid.color"] = "#d8b200"

    plt.rcParams["figure.facecolor"] = "#282828"
    plt.rcParams["figure.edgecolor"] = "black"

    plt.rcParams["savefig.facecolor"] = "black"
    plt.rcParams["savefig.edgecolor"] = "black"

    plt.rcParams["legend.edgecolor"] = "#d8b200"
    plt.rcParams["legend.facecolor"] = "#282828"

    plt.rcParams["boxplot.boxprops.color"] = "white"
    plt.rcParams["boxplot.capprops.color"] = "white"
    plt.rcParams["boxplot.flierprops.color"] = "white"
    plt.rcParams["boxplot.flierprops.markeredgecolor"] = "white"
    plt.rcParams["boxplot.whiskerprops.color"] = "white"


def create_plot(
    x_data: numpy_flt, y_data: list[numpy_flt], y_names: list[str]
) -> tuple[fig.Figure, Axes]:
    """Create line plot from simulation results"""

    # set style to look like an oscilloscope
    oscilloscope_colors()

    fig_axe: tuple[fig.Figure, Axes] = plt.subplots(figsize=FIG_SIZE)  # type: ignore
    axe: Axes = fig_axe[1]

    for index, y_array in enumerate(y_data):
        axe.plot(x_data, y_array, label=y_names[index])  # type: ignore

    plt.legend(title="Signals:")  # type: ignore

    return fig_axe


class Plot:
    """plot from simulation results"""

    def __init__(
        self,
        name: str,
        signals: list[numpy_flt],
        sig_names: list[str],
        results_path: Path,
    ) -> None:
        self.name = name
        self.signals = signals
        self.sig_names = sig_names
        self.results_path: Path = results_path

        # create initial plot
        self.fig_axe = create_plot(self.signals[0], self.signals[1:], self.sig_names)
        self.fig: fig.Figure = self.fig_axe[0]
        self.axe: Axes = self.fig_axe[1]

    def set_title(self, title: str) -> None:
        """title for plot"""
        self.axe.set_title(title) # type: ignore

    def define_axes(
        self, x_info: tuple[str, str, Scale], y_info: tuple[str, str, Scale]
    ) -> None:
        """Define the x,y axes' labels (measure & units) and scale (linear or log)

        Args:
            x_info (tuple[str, str, Scale]): (measure, units, scale)
            y_info (tuple[str, str, Scale]): (measure, units, scale)
        """
        x_measure = x_info[0]
        y_measure = y_info[0]
        x_units = x_info[1]
        y_units = y_info[1]
        x_scale: Scale = x_info[2]
        if x_scale not in ["linear", "log"]:
            x_scale = "linear"
        y_scale: Scale = y_info[2]
        if y_scale not in ["linear", "log"]:
            y_scale = "linear"

        self.axe.set_xlabel(f"{x_measure} ({x_units})") # type: ignore
        self.axe.set_ylabel(f"{y_measure} ({y_units})") # type: ignore
        self.axe.set_xscale(x_scale) # type: ignore
        self.axe.set_yscale(y_scale) # type: ignore

    def zoom(
        self,
        xmin: Optional[int | float] = None,
        xmax: Optional[int | float] = None,
        ymin: Optional[int | float] = None,
        ymax: Optional[int | float] = None,
    ) -> None:
        """Changes the range of x and y axis to plot"""
        if xmin is not None:
            self.axe.set_xlim(left=xmin)
        if xmax is not None:
            self.axe.set_xlim(right=xmax)

        if ymin is not None:
            self.axe.set_ylim(bottom=ymin)
        if ymax is not None:
            self.axe.set_ylim(top=ymax)

    def png(self) -> None:
        """Create a png of the plot and store in the "results_loc" dir"""
        plot_filename: Path = self.results_path / f"{self.name}.png"
        self.fig.savefig(str(plot_filename)) # type: ignore


def display_plots() -> None:
    """
    Display all plots to screen. These displays are different
    from the png's which are saved with a different method.
    """
    plt.show() # type: ignore
