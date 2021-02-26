from setuptools import setup, find_packages

setup (name="imqserver",
        version="1.1",
        description="Server package",
        author="Xyz",
        packages=find_packages(), install_requires = ['jsonpickle'])
