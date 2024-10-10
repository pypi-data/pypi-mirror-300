from setuptools import setup, find_packages

setup(
    name="FreddyApi",
    version="1.1.10",
    packages=find_packages(),
    install_requires=[],  # List your dependencies here
    author="Phillip Loacker",
    author_email="phillip.loacker@aitronos.com",
    description="A Python package for interacting with the Freddy API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Freddy-Development/aitronos-python-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
