#!/bin/bash

./stop.sh

xhost +local:root

docker run -t -d --privileged --net=host \
--name sofa \
-v $PWD/code:/home/noroot/code \
--env="DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
 sofa:docker
