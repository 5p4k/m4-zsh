#! /bin/zsh

# Turn on extended glob
setopt EXTENDED_GLOB

# Load all files but those ending in .disabled
for file in ~/.zsh/*~*.disabled; do
    source $file
done

source /home/5p4k/.iterm2_shell_integration.zsh
