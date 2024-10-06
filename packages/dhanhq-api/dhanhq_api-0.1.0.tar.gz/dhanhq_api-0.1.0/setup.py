from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dhanhq_api",
    version="0.1.0",
    author="Mani",
    author_email="",
    description="A Python client for the DhanHQ API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dhanhq_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.25.1",
        "pydantic>=1.8.2",
    ],
)