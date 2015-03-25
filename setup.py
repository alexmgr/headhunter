import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mlhead",
    version = "0.0.1",
    author = "Alex Moneger",
    author_email = "alexmgr@gmail.com",
    description = ("A tool to detect malicious HTTP connections by using "
                   "machine learning"),
    license = "GPL3",
    packages=["mlhead"],
    long_description=read('README.md'),
)
