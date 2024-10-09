from setuptools import setup

setup(
    name="basic_maths_011",             # Package name
    version="0.1",                 # Version number
    author="Mahesh A R",            # Author
    author_email="amaheshar@gmail.com",
    description="A simple maths package",
    long_description=open("README.md").read(),  # Load long description from README
    long_description_content_type="text/markdown",
    url="",  # Project URL (if any)
    packages=["basic_maths"],       # List of all Python import packages
    install_requires=[],           # List of dependencies          # Example dependency
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',       # Python version requirement
)
