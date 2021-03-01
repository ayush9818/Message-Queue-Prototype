from setuptools import setup, find_packages

setup (name="imqclient",
        version="1.0",
        description="Client package",
        author="Ayush Agarwal",
        packages=find_packages(), install_requires = ['jsonpickle'])
