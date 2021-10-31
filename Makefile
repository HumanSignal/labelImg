# ex: set ts=8 noet:

all: pyside6 test

test: testpy3

pyside6:
	pyside6-rcc -o libs/resources.py resources.qrc

testpy3:
	python3 -m unittest discover tests


clean:
	rm -rf ~/.labelImgSettings.pkl *.pyc dist labelImg.egg-info __pycache__ build

pip_upload:
	python3 setup.py upload

long_description:
	restview --long-description

.PHONY: all
