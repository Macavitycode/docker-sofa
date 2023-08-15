#!/bin/bash

if [ -z "$1" ]; then
    docker exec -it sofa bash
elif [ $1 == "detach" ]; then
    docker exec -t -d sofa bash -c /root/source_this.sh
fi
