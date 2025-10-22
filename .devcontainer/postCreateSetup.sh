#!/usr/bin/env bash
set -e

cp /workspaces/spicey01/dotfiles/vscode_bash_aliases /home/vscode/.bash_aliases
cp /workspaces/spicey01/dotfiles/vscode_bashrc /home/vscode/.bashrc

uv sync --locked
