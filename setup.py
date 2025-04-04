from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="thesr",
    version="0.0.12",
    license="gpl-3.0",
    author="John Hupperts",
    author_email="jrock4503@hotmail.com",
    description="thesaurus (and also dictionary)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/treatmesubj/Thesaurus_Rex",
    download_url="https://github.com/treatmesubj/Thesaurus_Rex/archive/refs/tags/v0.0.12.tar.gz",
    packages=["thesr"],
    package_dir={"Thesaurus_Rex": "thesr"},
    project_urls={
        "Source": "https://github.com/treatmesubj/Thesaurus_Rex",
    },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "rich",
    ],
)
