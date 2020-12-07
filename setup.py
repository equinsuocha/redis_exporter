from setuptools import setup, find_packages

setup(
    setup_requires=['setuptools>=17.1'],
    scripts=['bin/redis_exporter'],
    packages=find_packages()
)
