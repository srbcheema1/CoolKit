#!/usr/bin/env bash

_coolkit_args(){
    local cursor options
    options=$(coolkit list_args)
    cursor="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=( $(compgen -W "${options}" -- ${cursor}) )
    return 0
}
complete -F _coolkit_args coolkit
# source this file to use auto compeltion feature
# add to bashrc `source /path/to/this/file/arg.bash`
