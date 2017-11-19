
init python:
    import os


    def _getcwd():
        return os.getcwd()


    class Dummy(object):
        def foo(self):
            return True

init python:
    import os
    import renpy.exports as renpy  # NOQA
    from renpy.ui import Action  # NOQA
    from renpy.python import RevertableList  # NOQA


    def _getcwd():
        return os.getcwd()


    class Dummy(object):
        def foo(self):
            return True

init python:
    import os
    import renpy.exports as renpy  # NOQA
    from renpy.ui import Action  # NOQA


    def _getcwd():
        return os.getcwd()


    class Dummy(object):
        def foo(self):
            return True
