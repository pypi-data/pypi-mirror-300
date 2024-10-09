import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.2'
DESCRIPTION = 'Consolidation package for daily use'
LONG_DESCRIPTION = 'gqxls is an integration package for daily use'

setup(
    name="gqxls",
    version=VERSION,
    author="S Liao",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pillow','secrets','pymupdf','typing','openssl'],
    keywords=['python', 'gqxls'],
    python_requires='>=3.6',

)
