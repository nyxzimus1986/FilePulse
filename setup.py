#!/usr/bin/env python3
"""
FilePulse - A lightweight system-wide filesystem monitor
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="filepulse",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Cross-platform filesystem monitor with intelligent event classification, GUI interface, and resource-optimized real-time tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/filepulse",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/filepulse/issues",
        "Source Code": "https://github.com/yourusername/filepulse",
        "Documentation": "https://github.com/yourusername/filepulse#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "Environment :: X11 Applications",
    ],
    python_requires=">=3.8",
    keywords="filesystem monitor watchdog events real-time tracking gui cli",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "gui": [],  # GUI dependencies are already in main requirements
    },
    entry_points={
        "console_scripts": [
            "filepulse=filepulse.cli:main",
            "filepulse-gui=filepulse.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "filepulse": ["config/*.yaml", "config/*.json"],
    },
)
