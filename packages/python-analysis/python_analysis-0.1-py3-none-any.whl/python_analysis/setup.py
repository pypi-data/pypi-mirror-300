from setuptools import setup, find_packages

setup(
    name='python_analysis',  # Name of your package
    version='0.1',  # Initial version
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[  # External dependencies
        # e.g., 'pandas>=1.0.0', 'numpy>=1.19.2'
    ],
    description='A package for data analysis tasks',  # Short description
    author='Dhavasu',
    author_email='Dhava.mani@example.com',
    url='https://github.com/Dhava/python_analysis_package',  # Project URL
)
