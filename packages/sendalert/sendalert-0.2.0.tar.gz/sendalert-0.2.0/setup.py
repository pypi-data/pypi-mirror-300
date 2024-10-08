from setuptools import setup

setup(
    name="sendalert",
    version="0.2.0",
    packages=["sendalert"],
    install_requires=[
        "requests",
    ],
    author="philz1337x",
    author_email="python@okasi.de",
    description="A simple Python package for sending alerts using SendAlert.io",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/philz1337x/sendalert-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
