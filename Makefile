
all: resources.py

%.py: %.qrc
	pyrcc4 -o $@ $<

clean: $(shell git clean -fd)

