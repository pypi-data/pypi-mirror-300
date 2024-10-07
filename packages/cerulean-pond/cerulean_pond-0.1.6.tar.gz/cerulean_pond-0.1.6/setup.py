from setuptools import setup, find_packages

setup(
    name="cerulean_pond", 
    version="0.1.6",
    author="Malik Houni",
    author_email="malik.datascience@gmail.com",
    description="A library to create small datalakes called data ponds",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://ceruleanpond.com",  
    packages=find_packages(),  # Automatically find all packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # Changed to reflect All Rights Reserved
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
