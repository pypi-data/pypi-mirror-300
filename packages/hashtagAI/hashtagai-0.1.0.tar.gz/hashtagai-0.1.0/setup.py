from setuptools import setup, find_packages

setup(
    name="hashtagAI",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "exo=exo:main",  # This creates a command-line script named `exo`
        ],
    },)