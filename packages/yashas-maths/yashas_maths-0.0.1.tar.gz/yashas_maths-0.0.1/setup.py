from setuptools import setup, find_packages

setup(
    name="yashas_maths",  # Unique name for the package
    version="0.0.1",  # Initial version
    author="Yashas",  # Your name
    author_email="yashasdr007@gmail.com",  # Your email
    description="A simple Python package for basic arithmetic operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/s_modules",  # Project URL (if any)
    packages=find_packages(),  # Automatically finds all packages (i.e., s_modules)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum required Python version
)
