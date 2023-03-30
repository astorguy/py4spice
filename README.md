# Python for Spice
Lightweight Python interface to Ngspice

# Movtivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source circuit simulator with a command line interface (CLI). It's natural to use Python to interact with the CLI, making it easier to use Ngspice for advanced design analysis.

There exists a simulator called [PySpice](https://github.com/PySpice-org/PySpice) which embeds Ngspice through its API. ***Python for Spice***, on the other hand, is a lightweight module that facilitates Ngspice interaction. Simple classes and functions transparently create Ngspice netlists and commands. You can launch multiple analyses and convert the results to [Pandas](https://pandas.pydata.org/) and [Numpy](https://numpy.org/), enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/).

A modest knowledge of Ngspice and Python is assumed.

# Usage
***Python for Spice*** requires an Ngspice design, either in the form of a netlist or a [KiCad](https://www.kicad.org/) (version 7.0 or higher) schematic.

Ngspice can be used in many different ways. However, ***Python for Spice*** will interface to Ngspice only through the CLI in non-interactive mode. It creates a *control section* that will execute simulations in batch mode. Results from the simulation will be converted to [Pandas](https://pandas.pydata.org/) DataFrames.


# Typical Program Flow
A main Python program controls the flow. An example can be found [here](https://github.com/astorguy/bc546_amp).

1. import py4spice

1. Specify paths to KiCad and Ngspice executables, and project directory

1. Define signals of interest (node voltage, currents, etc.) with `Vectors` objects

1. Use a `KicadCmd` object to extract and condition a netlist from a schematic

1. Define one or more analyses (op, dc, tr, ac) with `Analyses` objects

1. A `Control` object defines the control section. The analyses and other control functions are part of it.

1. A `Simulation` Object is created and executed.

1. The tabular results from the simulation are converted to Pandas DataFrames

1. A `Plot` object can be used to encapsulate Matplotlib to view the results.

# Installation

1. install package:

`python -m pip install --upgrade py4spice`

2. Download this [example](https://github.com/astorguy/bc546_amp) (a bipolar amplifier) to try out the `py4spice` package.