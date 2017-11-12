import argparse

parser = argparse.ArgumentParser()
parser.add_argument("files", help="List of files to convert", nargs="+")

extra_indent = "    "


def py_to_rpy(filename):
    """Transpiles a Python file to a Ren'Py file.
    
    Creates a new .rpy file with an 'init python' block.

    """
    with open(filename + ".py", "r") as py_file:
        with open(filename + ".rpy", "w") as rpy_file:
            rpy_file.write("init python:")
            rpy_file.write("\n")
            for line in py_file:
                if line.strip():  # Line has content on it
                    rpy_file.write("{}{}".format(extra_indent, line))
                else:  # Line had only whitespace
                    rpy_file.write("\n")


if __name__ == "__main__":
    file_list = parser.parse_args().files
    for item in file_list:
        py_to_rpy(item)
