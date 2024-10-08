# setup.py
from setuptools import setup, find_packages

setup(
    name="jg_comp",
    version="0.1.4",
    author="Jacques Gariepy",
    description="A generic data compression package using dictionary-based and Huffman encoding techniques.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JacquesGariepy/jg-comp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
