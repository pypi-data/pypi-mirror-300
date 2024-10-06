from setuptools import setup, find_packages
from os import path

# Current working directory
cwd = path.abspath(path.dirname(__file__))


with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    try:
        long_description = f.read()
    except:
        long_description = None

setup(
    name='ansy',
    version='1.0.1',
    description='A Python package to colorize and format output in the terminal.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Anas-Shakeel/ansy',
    author='Anas Shakeel',
    license='MIT',
    packages=['ansy'],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ['ansy=ansy.cli:welcome']})
