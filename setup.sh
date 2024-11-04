#!/bin/bash

libs=("schedule")

for lib in ${libs[@]}; do
    pip3 install $lib || pip install $lib || { echo "Failed to install $lib" && exit 1; }
done

if [ -f ~/.zshrc ]; then
    run_zsh=-2
    if ! grep -q 'alias gitsync="python3 ~/githubSync/index.py"' ~/.zshrc; then
        echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.zshrc
        run_zsh=$((run_zsh + 1))
    fi
    # if ! grep -q 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' ~/.zshrc; then
    #     echo 'pgrep -f "nohup gitsync run:scheduler" > /dev/null || nohup gitsync run:scheduler &' >> ~/.zshrc
    #     run_zsh=$((run_zsh + 1))
    # fi
    if [ $run_zsh -gt 0 ]; then
        echo "Please restart your zsh shell or run 'source ~/.zshrc' to apply changes."
    fi
elif [ -f ~/.bashrc ]; then
    run_bash=-2
    if ! grep -q 'alias gitsync="python3 ~/githubSync/index.py"' ~/.bashrc; then
        echo 'alias gitsync="python3 ~/githubSync/index.py"' >> ~/.bashrc
        run_bash=$((run_bash + 1))
    fi
    # if ! grep -q 'pgrep -f "gitsync run:scheduler" > /dev/null || gitsync run:scheduler &' ~/.bashrc; then
    #     echo 'pgrep -f "nohup gitsync run:scheduler" > /dev/null || nohup gitsync run:scheduler &' >> ~/.bashrc
    #     run_bash=$((run_bash + 1))
    # fi
    if [ $run_bash -gt 0 ]; then
        echo "Please restart your bash shell or run 'source ~/.bashrc' to apply changes."
    fi
else
    echo "No .zshrc or .bashrc file found"
fi

