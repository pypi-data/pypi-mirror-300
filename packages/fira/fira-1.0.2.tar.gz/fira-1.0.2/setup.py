import codecs
import os
from setuptools import setup, find_packages

# you need to change all these
VERSION = '1.0.2'
DESCRIPTION = 'Fira, a plug-and-play memory-efficient training framework of LLMs.'


setup(
    name="fira",
    version=VERSION,
    author="xi chen",
    author_email="xichen.fy@gmail.com",
    url="https://github.com/xichen-fy/Fira",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'bitsandbytes',
        'tensorly',
    ],
    license="Apache 2.0",
    keywords=['python', 'optimizer', 'llms', 'linux', 'memory-efficient', 'training'],
)