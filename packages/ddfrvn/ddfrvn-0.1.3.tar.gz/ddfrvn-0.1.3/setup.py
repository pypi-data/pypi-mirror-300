from setuptools import setup, find_packages

setup(
    name="ddfrvn",
    version="0.1.3",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'xarray',
        'pandas',
        'geopandas',
    ],
    entry_points={
        'console_scripts': [
            'ddfr=DDFR.ddfr:main',
        ],
    },
    author="Francis Lapointe",
    author_email="francis.lapointe5@usherbrooke.ca",
    description="A CLI tool for downloading and processing Daymet NetCDF files for "
                "the Raven hydrological modelling framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Scriptbash/DaymetDownloaderForRaven",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="daymet, raven, hydrology",
    python_requires='>=3.6',
    project_urls={
        "Bug Reports": "https://github.com/Scriptbash/DaymetDownloaderForRaven/issues",
        "Funding": "https://ko-fi.com/scriptbash",
        "Source": "https://github.com/Scriptbash/DaymetDownloaderForRaven",
    },
)
