# Python-for-Spice (py4spice)
Lightweight Python package interface to Ngspice

## Motivation
[Ngspice](https://ngspice.sourceforge.io/) is an open source electrical circuit simulator. It typically executes in batch mode using an archaic script interface. The ***Python-for-Spice*** package facilitates Ngspice execution using Python scripts. You can launch multiple analyses and convert the results to [NumPy](https://numpy.org/) arrays, enabling downstream computation or plotting with [Matplotlib](https://matplotlib.org/). The motivation for Python-for-Spice is to access Ngspice from within a Python script, enabling advanced analysis of electrical circuits.

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
