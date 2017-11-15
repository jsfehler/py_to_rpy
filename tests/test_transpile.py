import os
import shutil

from ..py_to_rpy import py_to_rpy


def test_single_file(request):
    """Ensure the result of transpiling matches the pre-cooked file."""
    # Cleanup
    def fin():
        os.remove('dummy_file.rpy')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file')

    # The newly created .rpy file should match the expected file
    with open('expected_dummy_file.rpy') as expected_rpy_file:
        with open('dummy_file.rpy') as rpy_file:
            f1 = expected_rpy_file.read()
            f2 = rpy_file.read()
            assert f1 == f2


def test_strict(request):
    """When the strict option is used, then renpy imports are skipped."""
    # Cleanup
    def fin():
        os.remove('dummy_file_with_imports.rpy')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file_with_imports', strict=True)

    # The newly created file should not have the renpy imports
    with open('dummy_file_with_imports.rpy') as rpy_file:
        for line in rpy_file.readlines():
            assert '    import renpy.exports as renpy' != line
            assert '    from renpy.ui import Action' != line


def test_no_strict(request):
    """When the strict option is not used, then renpy imports are not skipped.
    """
    # Cleanup
    def fin():
        os.remove('dummy_file_with_imports.rpy')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file_with_imports')

    # The newly created file should still have the renpy imports
    with open('dummy_file_with_imports.rpy') as rpy_file:
        lines = rpy_file.readlines()
        assert '    import renpy.exports as renpy' == lines[2].rstrip()
        assert '    from renpy.ui import Action' == lines[3].rstrip()


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

    # The newly created folder should have the newly created file inside it
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

    # The existing folder should have the  newly created file inside it
    assert ['dummy_file.rpy'] == os.listdir('existing_dummy_folder')
