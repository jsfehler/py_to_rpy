import os
import shutil

from ..py_to_rpy import py_to_rpy
from ..py_to_rpy import combine_rpy_files
from ..py_to_rpy import remove_generated_files


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
            assert '    import renpy.exports as renpy  # NOQA' != line
            assert '    from renpy.ui import Action  # NOQA' != line


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
        assert '    import renpy.exports as renpy  # NOQA' == lines[2].rstrip()
        assert '    from renpy.ui import Action  # NOQA' == lines[3].rstrip()


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


def test_ignore(request):
    """Lines that are marked to be ignored should not be
    stripped out by strict mode.
    """
    # Cleanup
    def fin():
        os.remove('dummy_file_with_ignore.rpy')

    request.addfinalizer(fin)

    # Start test
    py_to_rpy('dummy_file_with_ignore', strict=True)

    # The newly created file should not have the renpy imports
    with open('dummy_file_with_ignore.rpy') as rpy_file:
        lines = rpy_file.readlines()
        assert '    from renpy.python import RevertableList  # NOQA' == lines[2].rstrip()


def test_minify(request):
    # Cleanup
    def fin():
        os.remove('final_file.rpy')

    request.addfinalizer(fin)

    # Start Test
    py_to_rpy('dummy_file')
    py_to_rpy('dummy_file_with_ignore')
    py_to_rpy('dummy_file_with_imports')

    combine_rpy_files(
        ['dummy_file', 'dummy_file_with_ignore', 'dummy_file_with_imports'],
        "final_file"
    )

    remove_generated_files(
        ['dummy_file', 'dummy_file_with_ignore', 'dummy_file_with_imports']
    )

    # The newly created .rpy file should match the expected file
    with open('expected_combined_file.rpy') as expected_rpy_file:
        with open('final_file.rpy') as rpy_file:
            f1 = expected_rpy_file.read()
            f2 = rpy_file.read()
            assert f1 == f2
