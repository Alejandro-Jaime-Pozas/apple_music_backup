#!/bin/bash

# Print debug information
echo "Starting backup script at $(date)" >> /Users/Alex/Library/Logs/applemusicbackup.out
echo "Current user: $(whoami)" >> /Users/Alex/Library/Logs/applemusicbackup.out
echo "Current directory: $(pwd)" >> /Users/Alex/Library/Logs/applemusicbackup.out

# Initialize pyenv
export PYENV_ROOT="/Users/Alex/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"

# Print Python path
echo "Python path: $(which python3)" >> /Users/Alex/Library/Logs/applemusicbackup.out

# Run the Python script with full path
/Users/Alex/.pyenv/versions/3.10.17/bin/python3 /Users/Alex/Documents/Coding/Applications/apple_music_library_copy/apple_music_backup.py
