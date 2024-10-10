from setuptools import setup, find_packages

setup(
    name="natural-agi-common",
    version="0.1.0",
    packages=find_packages(include=["common", "common.*", "common.model"]),
    install_requires=["pydantic"],
)
