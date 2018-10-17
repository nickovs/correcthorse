#!/usr/bin/env python3

# Setup file for correcthorse
import setuptools

import correcthorse

with open("README.md", "r") as fh:
    desc_lines = fh.readlines()
    stops = [i for i,l in enumerate(desc_lines) if "PyPI STOP" in l]
    if stops:
        desc_lines = desc_lines[:stops[0]]
    long_description = "".join(desc_lines)

setuptools.setup(
    name="correcthorse",
    version=correcthorse.__version__,
    author="Nicko van Someren",
    author_email="nicko@nicko.org",
    description="Secure but memorable passphrase generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickovs/correcthorse",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.4',
    keywords=['password', 'passphrase'],
    entry_points={
        'console_scripts': [
            'correcthorse = correcthorse.__main__:main'
        ]
    },
    include_package_data=True,
)
