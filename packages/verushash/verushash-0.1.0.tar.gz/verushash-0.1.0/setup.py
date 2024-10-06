from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="verushash",  # The name of your package
    version="0.1.0",  # Initial version
    author="Nathan Minnick",  # Your name
    author_email="minnicknathan47@gmail.com)",  # Your email
    description="Hash wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minnicknathan47/verushash",  # Link to your GitHub or project page
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)