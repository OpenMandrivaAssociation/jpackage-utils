#!/bin/sh
(cd `dirname $0` && lua -l abs2rel -e "print(abs2rel(\"$1\", \"$2\"))")

