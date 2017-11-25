import os

from ..py_to_rpy import cli


def test_cli_directory_parsing(request):
    """Ensure the glob implementation of directory parsing works."""
    # Cleanup
    def fin():
        os.remove('dummy_folder_with_multiple_files/dummy_file_1.rpy')
        os.remove('dummy_folder_with_multiple_files/dummy_file_2.rpy')

    request.addfinalizer(fin)

    # Start test
    cli.run(["dummy_folder_with_multiple_files/*.py"], None, False, None)

    assert 'dummy_file_1.rpy' in os.listdir('dummy_folder_with_multiple_files')
    assert 'dummy_file_2.rpy' in os.listdir('dummy_folder_with_multiple_files')


def test_cli_minify(request):
    """When using the minify option, the rpy files should be deleted and
       replaced with a combined file.
    """
    # Cleanup
    def fin():
        os.remove('minified.rpy')

    request.addfinalizer(fin)

    # Start test
    cli.run(["dummy_folder_with_multiple_files/*.py"], None, False, "minified")

    dir_list = os.listdir('dummy_folder_with_multiple_files')
    assert 'dummy_file_1.rpy' not in dir_list
    assert 'dummy_file_2.rpy' not in dir_list

    assert 'minified.rpy' in os.listdir()
