# setup.py
from setuptools import setup, find_packages

setup(
    name="unadd",          # Name of your library
    version="0.1",           # Initial version
    description="A simple mathematics library",
    author="Sonu",      # Your name
    author_email="sharmakakatua@gmail.com",  # Your contact info
    packages=find_packages(),  # Automatically find the packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version compatibility
)
