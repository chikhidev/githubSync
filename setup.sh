#!/bin/bash

libs=("schedule")

for lib in ${libs[@]}; do
    pip3 install $lib || pip install $lib || { echo "Failed to install $lib" && exit 1; }
done

if [ -f ~/.zshrc ]; then
    echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.zshrc
    zsh
elif [ -f ~/.bashrc ]; then
    echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.bashrc
    source ~/.bashrc
else
    echo "No .zshrc or .bashrc file found"
fi
fi
