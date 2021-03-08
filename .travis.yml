# vim: set ts=2 et:

# run xvfb with 32-bit color
# xvfb-run -s '-screen 0 1600x1200x24+32' command_goes_here

jobs:
  include:

    # Python 3 + QT5
    - os: linux
      dist: focal
      language: generic
      python: "3.6"
      env:
        - QT=5
        - CONDA=4.2.0
      addons:
        apt:
          packages:
            - cmake
            - xvfb
      before_install:
        # ref: https://repo.anaconda.com/archive/
        - curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
        # ref: http://conda.pydata.org/docs/help/silent.html
        - /bin/bash Anaconda3-2020.02-Linux-x86_64.sh -b -p $HOME/anaconda3
        - export PATH="$HOME/anaconda3/bin:$PATH"
        # ref: http://stackoverflow.com/questions/21637922/how-to-install-pyqt4-in-anaconda
        - conda create -y -n labelImg-py3qt5 python=3.6
        - source activate labelImg-py3qt5
        - conda install -y pyqt=5
        - conda install -y lxml
        - make qt5py3
        - xvfb-run make testpy3

    # Pipenv Python 3.7.5 + QT5 - Build .app
    - os: osx
      language: generic
      env:
        - PIPENV_VENV_IN_PROJECT=1
        - PIPENV_IGNORE_VIRTUALENVS=1
      install:
        - python3 --version
        - pip3 install pipenv
        - pipenv install pyqt5 lxml
        - pipenv run pip install pyqt5==5.13.2 lxml
        - pipenv run make qt5py3
        - rm -rf build dist
        - pipenv run python setup.py py2app
        - open dist/labelImg.app

script:
  - exit 0
