"""Setup configuration for TeamForge"""

from setuptools import setup, find_packages

setup(
    name="teamforge",
    version="1.0.0",
    description="Project Management CLI Tool",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "rich>=13.7.0",
        "tabulate>=0.9.0",
        "python-dateutil>=2.8.2",
        "colorama>=0.4.6",
        "pyfiglet>=0.8.post1",
    ],
    entry_points={
        "console_scripts": [
            "teamforge=main:main",
        ],
    },
    python_requires=">=3.8",
)