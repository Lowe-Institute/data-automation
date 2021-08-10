from setuptools import find_packages, setup

setup(
    name="lowe",
    url="https://www.lowe-institute.org/",
    version="0.0.1",
    author="Lowe Institute Automation Team",
    author_email="LoweLab@students.claremontmckenna.edu",
    maintainer="Abhinuv Uppal",
    maintainer_email="auppal22@students.claremontmckenna.edu",
    keywords = "macroeconomics data analysis statistics macro economics microeconomics micro scraping acs econometrics statistics econ api wrapper automation",
    license = "LICENSE.md",
    description="Automating data collection and processing for the Lowe Institute of Political Economy",
    long_description=open("README.md").read(),
    py_modules=[
        "lowe",
        "lowe.acs",
        "lowe.fred"
    ],
    install_requires=[
        "aiohttp",
        "aiolimiter",
        "asyncio",
        "backoff",
        "black==21.5b1",
        "datetime",
        "dvc[gdrive,gs]",
        "flake8",
        "matplotlib",
        "nbclient",
        "nbdime",
        "nbconvert",
        "nbdev",
        "nbformat",
        "notebook",
        "numpy",
        "pandas",
        "python-dotenv",
        "pytz",
        "ratelimit"
    ]

)