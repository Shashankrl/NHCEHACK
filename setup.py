"""
Setup file for the FundWise NLP package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fundwise-nlp",
    version="0.1.0",
    author="FundWise Development Team",
    author_email="example@fundwise.com",
    description="Financial news analysis and stock-related NLP system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fundwise-nlp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "nltk>=3.8.1",
        "scikit-learn>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "isort>=5.12.0",
        ],
        "api": [
            "flask>=2.3.3",
        ],
    },
) 