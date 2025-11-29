# Python-for-Spice (py4spice)
Lightweight Python package interface to Ngspice

## Motivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source electrical circuit simulator. It typically executes in batch mode using an archaic script interface. The ***Python-for-Spice*** package facilitates Ngspice execution using Python scripts. You can launch multiple analyses and convert the results to [NumPy](https://numpy.org/) arrays, enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/).

A modest knowledge of Ngspice and Python is required.

## Installation

### Install Ngspice
Ngspice must be [installed](https://ngspice.sourceforge.io/download.html). For most Linux distributions, ngspice can be installed with a package manager. As an example, for Debian use the following commands:

```bash
sudo apt update
sudo apt install ngspice
ngspice -v
```
### Install py4spice
py4spice is installed in the customary way for a PyPI package.
```bash
sudo apt update
sudo apt install py4spice
```
### Package Modules

| Module | Description |
|--------|-------------|
| `analyses` | Prepares analysis command that will go into control file and be executed during simulation |
| `control` | Generate control file to for a simulation |
| `kicad_netlist` | Create and execute a Kicad netlist export from a schematic |
| `netlist` | Create, modify, and combine netlists to prepare for an Ngspice simulation |
| `plot` | Matplotlib plot of numpy results from simulation |
| `print_section` | Section off text so it is easier to read in terminal |
| `sim_results` | Create objects for results extracted from simulation text files. Depending on the analysis type, the data are stored in different ways: either a plot or a table (dictionary) |
| `simulate` | Setup or run an Ngspice simulation |
| `step_info` | Perform variable measurements from step analyses. (i.e. rise-time, frequency, ...) |
| `vectors` | Vector set of signals for which to gather data, plot, ... |
| `waveforms` | Waveforms with a single x value and one or more y values in a 2D numpy array. Header defines the column names |

