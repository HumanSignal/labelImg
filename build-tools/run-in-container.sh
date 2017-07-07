#!/bin/sh
docker run -it --rm --workdir=$(pwd)/ --volume="/home/$USER:/home/$USER" tzutalin/py2qt4

