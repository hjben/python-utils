import setuptools
from pathlib import Path

setuptools.setup(
    name="hjben-python-utils",
    version="1.0.1",
    license='MIT',
    author="hjben",
    author_email="hj.ben.kim@gmail.com",
    description="Some utilities for data analysis with python",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    url="https://github.com/hjben/python-utils",
    packages=setuptools.find_packages(),
    install_requires=Path("requirements.txt").read_text().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English"
    ],
)