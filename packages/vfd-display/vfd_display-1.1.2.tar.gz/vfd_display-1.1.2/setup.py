from setuptools import setup, find_packages
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vfd-display',
    version='1.1.2',
    description='A module to interface with VFD displays via serial communication.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This tells PyPI to render the Markdown correctly
    author='DEVMNE',
    author_email='mne@yaposarl.ma',
    url='https://github.com/mnedev-cell/vfd-display',
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
