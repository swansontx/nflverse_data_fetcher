from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nflverse-data-fetcher",
    version="0.1.0",
    author="NFLverse Data Fetcher Contributors",
    description="Python library for fetching NFL data from NFLverse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swansontx/nflverse_data_fetcher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "pyarrow>=12.0.0",
        "requests>=2.31.0",
        "numpy>=1.24.0",
        "python-dateutil>=2.8.2",
    ],
)
