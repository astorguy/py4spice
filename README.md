# Python for Spice
Lightweight Python package interface to Ngspice

## Motivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source electrical circuit simulator. It typically executes in batch mode using an archaic script interface. The ***Python for Spice*** package facilitates Ngspice interaction. Its simple classes and functions transparently create Ngspice netlists and scripts. You can launch multiple analyses and convert the results to [NumPy](https://numpy.org/) arrays, enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/).

A modest knowledge of Ngspice and Python is required.

## SPICE and Ngspice
SPICE (Simulation Program with Integrated Circuit Emphasis) is one the most important software tools in the history of Silicon Valley. Originally released to the public in 1971, it can be argued that it is the oldest open source software still in use today. It is the trunk of a broad tree of commercial circuit simulators (e.g. [HSPICE®](https://www.synopsys.com/implementation-and-signoff/ams-simulation/primesim-hspice.html), [PSPICE®](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/analog-mixed-signal-simulation/pspice.html), [Spectre®](https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation.html), [LTSpice®](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html#learn), [QSPICE®](https://www.qorvo.com/design-hub/design-tools/interactive/qspice)). If you want to learn more about the history of SPICE, check out these lectures by original developers on YouTube: [The Life of SPICE](https://youtu.be/IkOb19FwgqY?si=HcTpD8ZNeK7JugDG), [
SPICE – 50 Years and One Billion Transistors Later](https://youtu.be/TQ8cJ9-GyGo?si=HEkz3La0uFJiHW9V).

Ngspice is the today's open source of the original SPICE. It's the simulation engine of several electronic design automation (EDA) programs. Knowledge of Ngspice gives you solid understanding of all SPICE derivatives.

## Typical Python Script Flow
The ***Python for Spice*** modules are used to help you control Ngspice with a Python script. The flow of the script will likely follow a simple three-stage structure:
1. Prepare the files required for simulation
1. Execute Ngspice simulation(s)
1. Convert the simulation results to dictionaries or NumPy arrays

