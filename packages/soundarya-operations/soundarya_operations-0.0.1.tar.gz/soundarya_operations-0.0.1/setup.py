from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="soundarya_operations",  # Your package name (must be unique on PyPI)
    version="0.0.1",  # Initial version
    author="Soundarya",
    author_email="soundaryar1008@gmail.com",
    description="A simple python package for basic arithmetic operations",
    long_description=long_description,
    long_description_content_type="text/markdown",  # or 'text/x-rst' for .rst files
    url="https://github.com/yourusername/my_package",  # URL of the project repository
    packages=find_packages(),  # Automatically find all packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3",  # Supported Python versions
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum required Python version
    install_requires=[        # Optional dependencies
        "requests",            # For example, list your package dependencies here
    ],
)
