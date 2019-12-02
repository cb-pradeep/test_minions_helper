import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minions_core",
    version="0.0.3",
    author="Mohan Rajan R",
    author_email="mohan.r@chargebee.com",
    description="Helper Clients & Functions for Microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cb-mohanr/minion-helpers",
    packages=["minions_core"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
