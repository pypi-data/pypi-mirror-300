from setuptools import setup, find_packages

setup(
    name="hashtagAI",
    version="0.2.1",
    packages=find_packages(),
    author="Thanabordee N. (Noun)",
    author_email="thanabordee.noun@gmail.com",
    install_requires=[  
        "openai",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ask=hashtagai:main",
                            ],
    },
        # Long description of your library
    readme = "README.md"
)