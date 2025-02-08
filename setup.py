from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="life-simulation",
    version="0.1.0",
    author="Jose LC",
    author_email="joselc@example.com",  # Replace with actual email
    description="A Python-based life simulation using a hexagonal grid system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joselc/life-sim-first-try",
    project_urls={
        "Bug Tracker": "https://github.com/joselc/life-sim-first-try/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Education",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'pygame',
        'numpy',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'mypy',
            'isort',
        ],
        'test': [
            'pytest',
            'pytest-cov',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'myst-parser',
        ],
    },
    entry_points={
        'console_scripts': [
            'life-sim=main:main',
        ],
    },
) 