# setup.py

import re
from setuptools import setup, find_packages


def get_version():
    with open("whiteduck/__init__.py", "r") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="whiteduck",
    version=get_version(),
    author="Andre Ratzenberger",
    author_email="andre.ratzenberger@whiteduck.com",
    description="A tool for scaffolding projects with the recommended tech stack of white duck",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/whiteduck",  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "whiteduck=whiteduck.cli:cli",  # Use 'cli' if using click
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
