# setup.py

from setuptools import setup, find_packages

setup(
    name="cypyscsi_gateway",
    version="0.1.0",
    description="A sample Python library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Martin Wambugu",
    author_email="info@cysecinnovation.com",
    url="https://github.com/yourusername/your_library",
    packages=find_packages(),
    install_requires=[],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
