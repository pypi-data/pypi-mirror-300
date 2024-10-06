import codecs
import os
from setuptools import setup, find_packages

# you need to change all these
VERSION = '1.0.0'
DESCRIPTION = 'Fira, a plug-and-play memory-efficient training framework of LLMs.'

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="fira",
    version=VERSION,
    author="xi chen",
    author_email="xichen.fy@gmail.com",
    url="https://github.com/xichen-fy/Fira",
    description=DESCRIPTION,
    license="Apache 2.0",
    keywords=['python', 'optimizer', 'llms', 'linux', 'memory-efficient', 'training'],
    install_requires=required,
)