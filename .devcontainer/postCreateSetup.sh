#!/usr/bin/env bash
set -e

cp /workspaces/py4spice/dotfiles/vscode_bash_aliases /home/vscode/.bash_aliases
cp /workspaces/py4spice/dotfiles/vscode_bashrc /home/vscode/.bashrc

uv sync --locked --editable
