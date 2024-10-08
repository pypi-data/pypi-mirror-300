#!/usr/bin/env python

from setuptools import setup

setup(
    name='dice_calc',
    version='0.0.5',
    author='Ar-Kareem',
    description='Advanced Calculator for Dice',
    package_dir={
        # main package 'src'
        'dice_calc': 'src',
        # parser 'src/parser'
        'dice_calc.parser': 'src/parser',
    },
    packages=['dice_calc'],    



)
