import os

from ..py_to_rpy import py_to_rpy


def test_py_to_rpy(request):
    """Ensure the result matches the pre-cooked file."""
    # Cleanup
    def fin():
        os.remove('dummy_file.rpy')

    request.addfinalizer(fin)    

    # Start test
    py_to_rpy('dummy_file')
    
    with open('expected_dummy_file.rpy') as expected_rpy_file:
        with open('dummy_file.rpy') as rpy_file:
            f1 = expected_rpy_file.read()
            f2 = rpy_file.read()
            assert f1 == f2
