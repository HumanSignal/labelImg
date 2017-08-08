# ex: set ts=8 noet:

all: qt4

test: testpy2

testpy2:
	python -m unittest discover tests

testpy3:
	python3 -m unittest discover tests

qt4: qt4py2

qt5: qt5py3

qt4py2:
	pyrcc4 -py2 -o resources.py resources.qrc

qt4py3:
	pyrcc4 -py3 -o resources.py resources.qrc

qt5py3:
	pyrcc5 -o resources.py resources.qrc

clean:
	rm -f .settings.pkl resources.pyc

.PHONY: test
