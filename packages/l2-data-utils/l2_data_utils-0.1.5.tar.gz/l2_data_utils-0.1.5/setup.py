from setuptools import setup, find_packages

setup(
    name='l2_data_utils',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'delta-spark',
    ],
)