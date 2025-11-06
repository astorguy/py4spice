# Python for Spice
Lightweight Python interface to Ngspice

# Movtivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source electrical circuit simulator. It typically executes in batch mode using an archaic script interface.  ***Python for Spice*** facilitates facilitates Ngspice interaction. Its simple classes and functions transparently create Ngspice netlists and scripts. You can launch multiple analyses and convert the results to [Numpy](https://numpy.org/) arrays, enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/).

A modest knowledge of Ngspice and Python is assumed.

# Usage
***Python for Spice*** requires an Ngspice design, either in the form of a netlist or a [KiCad](https://www.kicad.org/) (version 7.0 or higher) schematic.

Ngspice can be used in many different ways. However, ***Python for Spice*** will interface to Ngspice only through the CLI in non-interactive mode. It creates a *control section* that will execute simulations in batch mode. Results from the simulation are converted to [Numpy](https://numpy.org/) arrays.

Both Python scripts and Jupyter Notebooks are effcient ways to use ***Python for Spice***. Several examples are available in the [circuits](https://github.com/astorguy/py4spice/tree/main/circuits) directory.

# Typical Python script flow
There are three primary stages in the Python script using ***Python for Spice***:
1. Prepare to simulate
2. Simulate
3. Convert and analyze simulation results
