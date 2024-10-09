import sys
from setuptools import setup, find_packages
import pycinante

requirements = ["setuptools", "loguru", "loguru-mypy", "typing_extensions"]

setup(
    name="pycinante",
    version=pycinante.__version__,
    python_requires=">=3.8",
    author="Chisheng Chen",
    author_email="chishengchen@126.com",
    url="https://github.com/gndlwch2w/pycinante",
    description="Python rocinante (Pycinante) for easily programming in Python.",
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r", encoding=sys.getdefaultencoding()).read(),
    license="MIT-0",
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
)
