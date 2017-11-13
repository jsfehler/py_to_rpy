import os
import shutil

from ..py_to_rpy import py_to_rpy


def test_single_file(request):
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


def test_dest_option_new_folder(request):
    """Ensure the dest option works when the taget directory does not exist.
       New files should be placed in the dest folder.
    """
    # Cleanup
    def fin():
        shutil.rmtree('dummy_folder')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file', dest='dummy_folder')

    assert ['dummy_file.rpy'] == os.listdir('dummy_folder')


def test_dest_option_existing_folder(request):
    """Ensure the dest option works when the taget directory already exists.
       New files should be placed in the dest folder.
    """
    # Cleanup
    def fin():
        os.remove('existing_dummy_folder/dummy_file.rpy')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file', dest='existing_dummy_folder')

    assert ['dummy_file.rpy'] == os.listdir('existing_dummy_folder')
