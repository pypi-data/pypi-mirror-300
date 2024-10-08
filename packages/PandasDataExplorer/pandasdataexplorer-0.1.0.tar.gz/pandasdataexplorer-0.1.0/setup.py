from setuptools import setup, find_packages


# Read the contents of your README file to use as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PandasDataExplorer",  # Your package name
    version="0.1.0",  # Starting version number
    author="Ankur Zalavadiya",  # Add your name here
    author_email="heyankur19@gmail.com",  # Your email address
    description="A Python package for exploring and cleaning Pandas DataFrames",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Replace with your actual URL
    packages=find_packages(),  # Automatically find packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change to the correct license if needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Define the minimum Python version
    install_requires=[  # List your package dependencies
        "pandas>=1.2.0",
        "ydata_profiling>=3.0.0",
        "plotly>=5.0.0",
    ],
    include_package_data=True,  # To include non-Python files like README.md, etc.
    # You may add entry points if your package provides command-line tools
    # entry_points={
    #     'console_scripts': [
    #         'pandasexplorer=pandasdataexplorer:main',
    #     ],
    # },
)
