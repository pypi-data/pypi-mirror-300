from setuptools import setup

setup(
    name="byAd12-library",
    version="1.0",
    packages= ["byAd12"],
    description="Multi function library.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Adrián L. G. P.",
    author_email="adgimenezp@gmail.com",
    url="https://github.com/byAd12/byAd12-Library.git",
    install_requires=["ping3", "threading"]
)