"""Set up paths"""
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

add_path('libs')
