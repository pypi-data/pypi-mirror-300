from setuptools import setup, find_packages

setup(
    name="hashtagAI",
    version="0.1.21",
    packages=find_packages(),
    install_requires=[
        "openai",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "hash=hashtagai:main",  # This creates a command-line script named `hash`
        ],
    },
)