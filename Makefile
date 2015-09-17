
all: resources.py

%.py: %.qrc
	pyrcc4 -o $@ $<

