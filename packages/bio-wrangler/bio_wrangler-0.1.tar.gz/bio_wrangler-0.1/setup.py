# setup.py
from setuptools import setup, find_packages

setup(
    name="bio-wrangler",  # Package name
    version="0.1",  # Initial version
    author="Abdul-Rehman ikram",  # Author name
    description="A package for loading, transforming, and filtering bioinformatics datasets",
    packages=find_packages(),  # Automatically find all sub-packages
    install_requires=[  # Required dependencies
        "pandas",
        "biopython",
        "gffutils",
        "PyVCF3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify minimum Python version
)
