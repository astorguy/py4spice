"""Line plot multiple pd.DataFrame results from simulation
"""
from pathlib import Path
from typing import TypeAlias, Optional, Literal
import pandas as pd
import numpy as np
import numpy.typing as npt
import matplotlib.figure as fig  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.style  # type: ignore
from .vectors import Vectors

# type aliases
Scale = Literal["linear", "log"]

# size of figures to display. set size to match screen monitor size
FIG_SIZE: tuple[float, float] = (16, 8)

PLOT_STYLE_FILE: str = "./oscilloscope.mplstyle"  # style definition

# Alias for type checking
numpy_floats: TypeAlias = npt.NDArray[np.float64]
list_of_numpys: TypeAlias = list[numpy_floats]


def df_to_columns(dfr: pd.DataFrame) -> list_of_numpys:
    """Convert dataframe of sim results to a list of numpys (one for each column)

    Args:
        dfr (pd.DataFrame): simulation results

    Returns:
        list_of_numpys: a numpy array for each column (signal)
    """
    numpys: list_of_numpys = []
    column_names: list[str] = list(dfr.columns.values)
    for name in column_names:
        numpys.append(dfr[[name]].to_numpy())
    return numpys


def cols_to_curves(
    list_of_col: list_of_numpys, col_names: list[str], axe: plt.Axes
) -> None:
    """create curves from a list of numpy arrays

    Args:
        list_of_col (list_of_numpys):
        col_names (list[str]):
        axe (plt.Axes): plot object
    """
    x_array: numpy_floats = list_of_col[0]  # x-axis is the first column

    index: int = 1
    for y_array in list_of_col[1:]:
        axe.plot(x_array, y_array, label=col_names[index])
        index += 1


def create_plot(
    sim_results: pd.DataFrame, my_vectors: Vectors
) -> tuple[fig.Figure, plt.Axes]:
    """Create line plot from simulation results"""

    # set style to look like an oscilloscope
    matplotlib.style.use(PLOT_STYLE_FILE)

    fig_axe: tuple[fig.Figure, plt.Axes] = plt.subplots(figsize=FIG_SIZE)
    axe: plt.Axes = fig_axe[1]

    # reduce number of vectors to plot
    x_axis = [str(sim_results.columns[0])]
    column_names: list[str] = x_axis + my_vectors.list_out()
    subset_sim_results: pd.DataFrame = sim_results[column_names]

    # convert to numpy arrays
    columns: list_of_numpys = df_to_columns(subset_sim_results)
    cols_to_curves(columns, column_names, axe)

    plt.legend(title="Signals:")

    return fig_axe


class Plot:
    """plot from simulation results"""

    def __init__(
        self,
        name: str,
        sim_data: pd.DataFrame,
        vectors: Vectors,
        results_path: Path,
    ) -> None:
        self.name: str = name
        self.sim_data: pd.DataFrame = sim_data
        self.vectors: Vectors = vectors
        self.results_path: Path = results_path

        # create initial plot
        self.fig_axe: tuple[fig.Figure, plt.Axes] = create_plot(sim_data, self.vectors)
        self.fig: fig.Figure = self.fig_axe[0]
        self.axe: plt.Axes = self.fig_axe[1]

    def set_title(self, title: str) -> None:
        """title for plot"""
        self.axe.set_title(title)

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

        self.axe.set_xlabel(f"{x_measure} ({x_units})")
        self.axe.set_ylabel(f"{y_measure} ({y_units})")
        self.axe.set_xscale(x_scale)
        self.axe.set_yscale(y_scale)

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
        self.fig.savefig(str(plot_filename))


def display_plots() -> None:
    """
    Display all plots to screen. These displays are different
    from the png's which are saved with a different method.
    """
    plt.show()
