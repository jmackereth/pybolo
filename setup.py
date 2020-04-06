import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybolo-jmackereth", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="tedmackereth@gmail.com",
    description="A simple python interface for Luca Casagrande's bolometric-corrections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmackereth/pybolo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
