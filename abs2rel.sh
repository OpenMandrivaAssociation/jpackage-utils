#!/bin/sh
if [ $# -ne 2 ]; then
    echo "usage: $0 <PATH> <BASE>" >&2
    exit 1
fi

exec lua "`dirname "$0"`/abs2rel.lua" "$@"
