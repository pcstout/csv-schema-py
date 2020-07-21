import setuptools
from src.csv_schema._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv-schema",
    version=__version__,
    author="Patrick Stout",
    author_email="pstout@prevagroup.com",
    license="Unknown",
    description="CSV file validation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcstout/csv-schema-py",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=(
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            "csv-schema = csv_schema.cli:main"
        ]
    },
    install_requires=[

    ]
)
