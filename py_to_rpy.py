import argparse
import errno
import os

parser = argparse.ArgumentParser()
parser.add_argument("files", help="List of files to convert", nargs="+")
parser.add_argument(
    "--dest",
    help="The folder to place transpiled files into",
    nargs="?"
)

extra_indent = "    "


def py_to_rpy(filename, dest=None):
    """Transpiles a Python file to a Ren'Py file.

    Creates a new .rpy file with an 'init python' block.

    Args:
        dest (string): The folder to place transpiled files into.
    
    """
    if dest:
        dest_string = "{}/".format(dest)
        # Create the dist directory if it doesn't already exist
        try:
            os.makedirs(dest)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        dest_string = ""

    rpy_file_location = "{}{}.rpy".format(dest_string, filename)
    
    with open(filename + ".py", "r") as py_file:
        with open(rpy_file_location, "w") as rpy_file:
            rpy_file.write("init python:")
            rpy_file.write("\n")
            for line in py_file:
                if line.strip():  # Line has content on it
                    rpy_file.write("{}{}".format(extra_indent, line))
                else:  # Line had only whitespace
                    rpy_file.write("\n")


if __name__ == "__main__":
    file_list = parser.parse_args().files
    dest_dir = parser.parse_args().dest
    for item in file_list:
        py_to_rpy(item, dest=dest_dir)
