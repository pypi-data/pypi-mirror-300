from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pydeepflow",
    version="0.1.4",  # Updated version
    author="Ravin D",
    author_email="ravin.d3107@outlook.com",
    description="A deep learning package optimized for performing Deep Learning Tasks, easy to learn and integrate into projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravin-d-27/PyDeepFlow",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy==1.23.5",
        "pandas==1.5.3",
        "scikit-learn==1.2.0",
        "jupyter==1.0.0",
        "tqdm==4.64.1",
        "colorama==0.4.6",
    ],
)
