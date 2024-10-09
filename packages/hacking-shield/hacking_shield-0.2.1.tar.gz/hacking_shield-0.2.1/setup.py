from setuptools import setup, find_packages
import os

# Read the contents of your README file for the long description
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name="hacking_shield",
    version="0.2.1",
    description="Client for detecting harmful SQL queries using a third-party API",
    long_description=read_readme(),  # Include the contents of README.md
    long_description_content_type='text/markdown',  # Specify the format of the long description
    author="Kondwani Nyirenda",
    author_email="kondwaninyirenda99@gmail.com",
    url="https://github.com/kondwani0099/hacking-shield",  # Add your GitHub URL or project homepage
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",  # Ensures 'requests' is installed as a dependency
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
