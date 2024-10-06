from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.4"
DESCRIPTION = "A simple Python wrapper for the some-random-api.ml API."
LONG_DESCRIPTION = "Easily access animal images and facts in your Python projects."

project_urls = {
    "Bug Tracker": "https://github.com/DARKPOISON-yt/animalapi/issues",
    "Source Code": "https://github.com/DARKPOISON-yt/animalapi",
}

setup(
    name="animalapi",
    version=VERSION,
    author="Ashutosh Das",
    author_email="ashutoshdas2004@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests","random"],
    keywords=["animal", "api", "wrapper", "images", "facts"],
    project_urls=project_urls,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)