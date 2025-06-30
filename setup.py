from setuptools import setup, find_packages

setup(
    name="toger",
    version="0.1.1",
    description="A Python package for the toger project.",
    author="Bogdan Boris",
    author_email="gdrghdhgddy@gmail.com",
    url="https://github.com/Bogdan-godot/toger-api",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "pydantic==2.10.6"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)