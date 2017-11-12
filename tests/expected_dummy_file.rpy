init python:
    import os

    def _getcwd():
        return os.getcwd()

    class Dummy(object):
        def foo(self):
            return True
