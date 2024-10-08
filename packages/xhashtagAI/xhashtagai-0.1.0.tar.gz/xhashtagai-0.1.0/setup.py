from setuptools import setup, find_packages
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''
setup(
    name="xhashtagAI",
    version="0.1.0",
    packages=find_packages(where="."),
    py_modules=["xhashtagAI", "__init__"],
    author="Thanabordee N. (Noun)",
    author_email="thanabordee.noun@gmail.com",
    install_requires=[  
        "openai",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "x=xhashtagAI:main",
                            ],
    },
        # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown'
)