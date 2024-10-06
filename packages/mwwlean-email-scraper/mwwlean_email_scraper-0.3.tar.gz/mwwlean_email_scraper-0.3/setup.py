from setuptools import setup, find_packages

setup(
    name='mwwlean_email_scraper',
    version='0.3',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "email_scraper = mwwlean_email_scraper:main",
        ],
    }
)