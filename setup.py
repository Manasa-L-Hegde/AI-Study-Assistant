"""
Setup script for AI Study Assistant.
This file is used for package installation and distribution.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()

setup(
    name="ai-study-assistant",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive AI-powered study assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AI-Study-Assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-study-assistant=main:main",
        ],
    },
    include_package_data=True,
    keywords="ai education study assistant learning quiz groq llm",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/AI-Study-Assistant/issues",
        "Source": "https://github.com/yourusername/AI-Study-Assistant",
        "Documentation": "https://github.com/yourusername/AI-Study-Assistant/tree/main/docs",
    },
)

# Made with Bob
