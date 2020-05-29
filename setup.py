import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv-schema",
    version="0.0.b0",
    author="Patrick Stout",
    author_email="pstout@prevagroup.com",
    license="Unknown",
    description="CSV file validation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/covid-open-data/csv-schema-py",
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
