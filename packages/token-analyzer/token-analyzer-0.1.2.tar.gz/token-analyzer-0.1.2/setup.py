from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="token-analyzer",  # Name of your package
    version="0.1.2",  # Initial version
    author="Tarun Kr. Singh",
    author_email="krtarunsingh@gmail.com",
    description="A Python library for analyzing and calculating token usage costs for various LLM models like OpenAI and Anthropic, with support for real-time currency conversion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krtarunsingh/token_analyzer",  # GitHub repo or project page
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[
        "freecurrencyapi",
        "logging"
    ],
)
