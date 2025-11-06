# Python for Spice
Lightweight Python package interface to Ngspice

# Movtivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source electrical circuit simulator. It typically executes in batch mode using an archaic script interface. The ***Python for Spice*** package facilitates Ngspice interaction. Its simple classes and functions transparently create Ngspice netlists and scripts. You can launch multiple analyses and convert the results to [Numpy](https://numpy.org/) arrays, enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/).

A modest knowledge of Ngspice and Python is required.

# SPICE and Ngspice
SPICE (Simulation Program with Integrated Circuit Emphasis) is one the most important software tools in the history of Silicon Valley. Originally released to the public in 1971, it can be argued that it is the oldest open source software still in use today. It is the root of a broad tree of commercial circuit simulators (i.e. [HSPICE®](https://www.synopsys.com/implementation-and-signoff/ams-simulation/primesim-hspice.html), [PSPICE®](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/analog-mixed-signal-simulation/pspice.html), [Spectre®](https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation.html), [LTSpice®](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html#learn), [QSPICE®](https://www.qorvo.com/design-hub/design-tools/interactive/qspice)). Ngspice is the today's open source of the original SPICE. It is the simulation engine integrated into many electrical CAD programs (i.e.). Knowledge of Nspice will give you proficency in all commercial circuit simulators.

