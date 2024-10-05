from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="argparse-history",
    version="0.2.1",
    author="Dimitry Khvorostyanov",
    author_email="dimitry.khvorostyanov@locean.ipsl.fr",
    description="An extension of argparse with history tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimitrix-cnrs/argparse-history",
    py_modules=["argparse_h"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="argparse history command-line",
    python_requires=">=3.8",
)
