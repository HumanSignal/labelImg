
all: qt4

qt4: qt4py2

qt5: qt4py3

qt4py2:
	pyrcc4 -py2 -o resources.py resources.qrc

qt4py3:
	pyrcc4 -py3 -o resources.py resources.qrc

qt5py3:
	pyrcc5 -o resources.py resources.qrc

