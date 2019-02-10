# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ballooncatheterization',
    version='0.1.0',
    description='Training GUI written in Python 3',
    long_description=readme,
    author='Nam Tran, Cooper Pearson, Richie Beck, Marcel Isper, Brianna Cathey',
    author_email='tranngocnam97@gmail.com',
    url='https://github.com/omn0mn0m/Dungeon-Crawler-2',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
