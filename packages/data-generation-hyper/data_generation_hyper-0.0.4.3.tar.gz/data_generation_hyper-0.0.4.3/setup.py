from setuptools import setup, find_packages

setup(
    name="data_generation_hyper",
    version="0.0.4.3",
    author="Cesare Bidini, Onuralp Guvercin, Emin Yuksel, Mevlut",
    author_email="cesare.bidini@gmail.com",
    description="Library for synthetic data generation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cesbid/data_generation",  # Your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)