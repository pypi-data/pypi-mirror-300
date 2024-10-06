from setuptools import find_packages, setup

setup(
    name='pytranscripts',
    packages=find_packages(include = ['pytranscripts']),
    version='0.1.0',
    description='A python package for extracting electronic health transcripts ,  and then classifying them based on human annotated data.',
    author='eskayML',
)