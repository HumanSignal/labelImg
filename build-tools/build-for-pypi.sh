#!/bin/sh
# Packaging
cd ..;sudo python setup.py sdist;sudo python setup.py install

# Release
# python setup.py register
# python setup.py sdist upload
