"""Setup.py"""
from setuptools import setup, find_packages

INSTALL_REQUIRES = ["scrapy", "google-cloud-pubsub"]

EXTRAS_REQUIRE = {
    "test": ["pytest", "pytest-clarity", "black", "flake8", "pylint"],
    "dev": ["tox"],
}

EXTRAS_REQUIRE["dev"] += EXTRAS_REQUIRE["test"]

setup(
    name="scrapy-pubsub",
    version="0.0.2",
    description="Scrapy item pipeline for Cloud Pub/Sub.",
    author="Yacine Nouri",
    author_email="yacine@nouri.io",
    url="https://github.com/ynouri/scrapy-pubsub/",
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    setup_requires=[],
    python_requires=">=3.6",
    extras_require=EXTRAS_REQUIRE,
    py_modules=["scrapy_pubsub"],
    zip_safe=False,
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
