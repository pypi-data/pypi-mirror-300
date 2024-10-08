from setuptools import setup, find_packages

setup(
    name='etem_utils',  # Package name
    version='0.0.1',  # Dummy version
    description='Dummy package for reserving the name etem_utils on PyPI',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['reserved.txt']},  # Including the text file in the package
)