#!/bin/bash

if [ -f ~/.zshrc ]; then
    echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.zshrc
    zsh
else if [ -f ~/.bashrc ]; then
    echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.bashrc
    source ~/.bashrc
else
    echo "No .zshrc or .bashrc file found"
fi
fi
