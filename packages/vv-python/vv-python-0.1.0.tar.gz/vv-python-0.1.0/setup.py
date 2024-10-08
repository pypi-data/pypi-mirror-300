from setuptools import setup, find_packages

setup(
    name="vv-python",
    version="0.1.0",
    author="Vincent Viljoen",
    author_email="your.email@example.com",
    description="Testing custom python packages",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
