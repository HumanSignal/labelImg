#!/bin/bash
PS3='Select the supported images: '
options=("py2qt4" "py3qt5" "Quit")
IMAGE=tzutalin/py2qt4
select opt in "${options[@]}"
do
    case $opt in
        "py2qt4")
            IMAGE=tzutalin/py2qt4
            break
            ;;
        "py3qt5")
            IMAGE=tzutalin/py3qt5
            break
            ;;
        "Quit")
            exit 0
            ;;
        *) echo invalid option;;
    esac
done

echo $IMAGE

docker run -it \
    --user $(id -u) \
    -e DISPLAY=unix$DISPLAY \
    --workdir=$(pwd) \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    $IMAGE

