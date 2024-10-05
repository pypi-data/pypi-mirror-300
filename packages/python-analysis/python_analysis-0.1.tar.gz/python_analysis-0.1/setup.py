from setuptools import setup, find_packages

setup(
    name='python_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'scipy',
    ],
    description='A data analysis package for cleaning, visualization, and statistics.',
    author='Dhavasu',
)
