from setuptools import setup, find_packages

setup(
    name="emji_ascvd_calculator",
    version="0.1.0",
    author="Eslam Mohamed Jaber Elmasry",
    author_email="emji555@gmail.com",
    description="ASCVD risk calculator based on user input parameters",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emji555/ascvd_calculator",  # replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
