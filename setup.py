from setuptools import setup

from setuptools import find_packages

INSTALL_REQUIRE = [
    "requests[socks]>=2.32.3",
    "bs4==0.0.1",
    "pydantic==2.9.2",
    "tqdm==4.66.3",
    "brotli==1.1.0",
]

cli_reqs = ["click==8.1.3", "rich==13.9.2"]

EXTRA_REQUIRE = {
    "cli": cli_reqs,
    "all": cli_reqs + [],
}

setup(
    name="fzmovies-api",
    version="0.1.5",
    license="GPLv3",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="Unofficial Python API/SDK for fzmovies.net",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/Simatwa/fzmovies-api",
    project_urls={
        "Bug Report": "https://github.com/Simatwa/fzmovies-api/issues/new",
        "Homepage": "https://github.com/Simatwa/fzmovies-api",
        "Source Code": "https://github.com/Simatwa/fzmovies-api",
        "Issue Tracker": "https://github.com/Simatwa/fzmovies-api/issues",
        "Download": "https://github.com/Simatwa/fzmovies-api/releases",
        "Documentation": "https://github.com/Simatwa/fzmovies-api/",
    },
    entry_points={
        "console_scripts": [
            "fzmovies = fzmovies_api.console:main",
        ],
    },
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    python_requires=">=3.10",
    keywords=[
        "movies",
        "fzmovies",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
