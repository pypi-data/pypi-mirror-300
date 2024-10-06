from distutils.core import setup
from setuptools import find_packages

setup(
    name='unstable_baselines3',
    packages=find_packages(),
    install_requires=[
        'gymnasium',
        'pettingzoo',
        'torch',
        'stable-baselines3',
    ],
)
