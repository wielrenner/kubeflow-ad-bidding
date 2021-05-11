import os

from setuptools import setup, find_packages


setup(
    name='kubeflow-bandit',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=["Flask", "numpy", "gunicorn"],
    description='',
)