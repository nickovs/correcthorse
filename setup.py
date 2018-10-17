# Setup file for unificontrol
import setuptools

import correcthorse

setuptools.setup(
    name="correcthorse",
    version=correcthorse.__version__,
    author="Nicko van Someren",
    author_email="nicko@nicko.org",
    description="Secure but memorable passphrase generator",
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
    }
)
