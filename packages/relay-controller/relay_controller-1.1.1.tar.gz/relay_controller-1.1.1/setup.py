from setuptools import setup, find_packages
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='relay-controller',
    version='1.1.1',
    author='DEVMNE',
    author_email='mne@yaposarl.ma',
    url='https://github.com/mnedev-cell/relay_controller',
    description='A relay controller module for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This tells PyPI to render the Markdown co
    packages=find_packages(),
    install_requires=[
        'pyhid-usb-relay',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
