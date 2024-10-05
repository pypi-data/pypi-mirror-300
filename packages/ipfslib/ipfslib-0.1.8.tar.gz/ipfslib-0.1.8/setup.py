from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


setup(
    name=           "ipfslib",
    version=        "0.1.8",
    author=         "Christian Remboldt",
    author_email=   "christian@remboldt.eu",
    description=    "IPFS Library for Python",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ipfs', 'api', 'decentral', 'networking', 'ipns', 'web3'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)



