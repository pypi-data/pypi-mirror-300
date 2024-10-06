from setuptools import setup, find_packages

setup(
    name='mwwlean_email_scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "email_scraper = email_scraper:main",
        ],
    }
)