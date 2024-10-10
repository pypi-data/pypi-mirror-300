from setuptools import setup, find_packages

setup(
    name='vfd-display',
    version='1.1.1',
    description='A module to interface with VFD displays via serial communication.',
    packages=find_packages(),
    author='DEVMNE',
    author_email='mne@yaposarl.ma',
    url='https://github.com/mnedev-cell/qr_code_reader',
    install_requires=[
        'pyserial',  # Add any other dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
