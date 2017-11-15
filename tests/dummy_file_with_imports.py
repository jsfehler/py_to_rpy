import os
import renpy.exports as renpy
from renpy.ui import Action


def _getcwd():
    return os.getcwd()


class Dummy(object):
    def foo(self):
        return True
