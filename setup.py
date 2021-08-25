from setuptools import setup

setup(
    name="lowe",
    url="https://www.lowe-institute.org/",
    version="0.0.1",
    author="Lowe Institute Automation Team",
    author_email="LoweLab@students.claremontmckenna.edu",
    maintainer="Abhinuv Uppal",
    maintainer_email="auppal22@students.claremontmckenna.edu",
    keywords="macroeconomics data analysis statistics macro economics\
        microeconomics micro scraping acs econometrics\
        statistics econ api wrapper automation",
    license="LICENSE.md",
    description="Automating data collection and processing\
        for the Lowe Institute of Political Economy",
    long_description=open("README.md").read(),
    py_modules=["lowe", "lowe.acs", "lowe.fred", "lowe.edd"],
    install_requires=[
        "aiohttp",
        "aiolimiter",
        "backoff",
        "bidict",
        "black==21.7b0",
        "datetime",
        "dvc[gdrive,gs]",
        "flake8==3.9.2",
        "matplotlib",
        "nbclient",
        "nbdime",
        "nbconvert",
        "nbdev",
        "nbformat",
        "notebook",
        "numpy",
        "openpyxl",
        "pandas",
        "pandasql",
        "python-dotenv",
        "pytz",
        "ratelimit",
        "us",
    ],
)
