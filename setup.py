from os.path import join, dirname

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(
    name='chart-museum-cleaner',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='',
    author='fd',
    author_email='',
    description='Remove unused helm charts in chart museum',
    install_requires=install_requires,
    long_description=open('README.md').read(),
    entry_points={'console_scripts': 'chart-museum-cleaner = chart_museum_cleaner.cli:main'},
)
