from setuptools import setup

setup(
    name="py_to_rpy",
    version="0.9",
    description="Convert Python files to Ren'Py files",
    url="https://github.com/jsfehler/py_to_rpy",
    author="Joshua Fehler",
    author_email="jsfehler@gmail.com",
    license="MIT",
    packages=['py_to_rpy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'py_to_rpy = py_to_rpy.cli:main'
        ]
    }
)
