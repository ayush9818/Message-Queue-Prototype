from setuptools import setup, find_packages

setup (name="imqclient",
        version="1.1",
        description="Client package",
        author="Xyz",
        packages=find_packages(), install_requires = ['jsonpickle'])
