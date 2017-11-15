import os
import renpy.exports as renpy  # NOQA
from renpy.ui import Action  # NOQA


def _getcwd():
    return os.getcwd()


class Dummy(object):
    def foo(self):
        return True
