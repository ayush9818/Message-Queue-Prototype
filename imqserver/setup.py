from setuptools import setup, find_packages

setup (name="imqserver",
        version="1.0",
        description="Server package",
        author="Ayush Agarwal",
        packages=find_packages(), install_requires = ['jsonpickle'])
