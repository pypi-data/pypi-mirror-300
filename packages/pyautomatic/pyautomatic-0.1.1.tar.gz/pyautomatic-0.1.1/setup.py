from setuptools import setup, find_packages

setup(
    name="pyautomatic",
    version="0.1.1",
    description="pyautomatic",
    author="xiaobl",
    author_email="monios114514@outlook.com",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21",
        "requests>=2.26",
    ],
)

