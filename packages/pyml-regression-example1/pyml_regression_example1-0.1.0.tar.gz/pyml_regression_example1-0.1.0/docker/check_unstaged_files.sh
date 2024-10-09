#!/bin/bash

script_dir=$(pwd)

cd ..  # Need to be in the root of the repository for git commands to work

# Check for unstaged files
unstaged_files=$(git diff --name-only)

# Check for untracked files
untracked_files=$(git ls-files --others --exclude-standard)

# Check for staged but uncommitted files
staged_files=$(git diff --cached --name-only)

if [ -n "$unstaged_files" ] || [ -n "$untracked_files" ] || [ -n "$staged_files" ]; then
    echo "You have unstaged, untracked, or staged (but uncommitted) files:"

    if [ -n "$unstaged_files" ]; then
        echo "Unstaged files:"
        echo -e "\e[31m$unstaged_files\e[0m"
        fi

    if [ -n "$untracked_files" ]; then
        echo "Untracked files:"
        echo -e "\e[31m$untracked_files\e[0m"
    fi

    if [ -n "$staged_files" ]; then
        echo "Staged but uncommitted files:"
        echo -e "\e[32m$staged_files\e[0m"
    fi

    read -p "Do you want to add unstaged and untracked files? (y/n) [y]: " -n 1 -r
    echo
    # Treat empty input as 'y'
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        git add $unstaged_files $untracked_files
        echo "Unstaged and untracked files were added."
    else
        echo "No files were added."
    fi
else
    echo "No unstaged, untracked, or staged files found."
fi
