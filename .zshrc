#! /bin/zsh

# Turn on extended glob
setopt EXTENDED_GLOB
setopt AUTO_CD
setopt CORRECT
setopt PUSHD_TO_HOME
setopt AUTO_PUSHD
setopt AUTO_LIST

# Load all files but those ending in .disabled
for file in ~/.zsh/*~*.disabled; do
    source $file
done

MAN_POSIXLY_CORRECT=1; export MAN_POSIXLY_CORRECT
