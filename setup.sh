#!/bin/bash

libs=("schedule")

for lib in ${libs[@]}; do
    pip3 install $lib || pip install $lib || { echo "Failed to install $lib" && exit 1; }
done

if [ -f ~/.zshrc ]; then
    if ! grep -q 'alias gitsync="python3 ~/githubSync/index.py"' ~/.zshrc; then
        echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.zshrc
    fi
    if ! grep -q 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' ~/.zshrc; then
        echo 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' >> ~/.zshrc
    fi
    zsh

elif [ -f ~/.bashrc ]; then
    run_bash
    if ! grep -q 'alias gitsync="python3 ~/githubSync/index.py"' ~/.bashrc; then
        echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.bashrc
    fi
    if ! grep -q 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' ~/.bashrc; then
        echo 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' >> ~/.bashrc
    fi
    source ~/.bashrc
else
    echo "No .zshrc or .bashrc file found"
fi
fi
