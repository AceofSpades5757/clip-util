import setuptools


with open("README.md", "r", encoding="utf-8") as fin:
    long_description = fin.read()


build_requires = [
    "wheel",
    "setuptools",
]
test_requires = [
    "tox",
    "tox-gh-actions",
]
dev_requires = (
    build_requires
    + test_requires
    + [
        # CI/CD Tool - Runs formatting tools
        "pre-commit",
        # Type Checker
        "mypy",
    ]
)


setuptools.setup(
    name="clip-util",
    version="0.1.17",
    author="Kyle L. Davis",
    author_email="aceofspades5757.github@gmail.com",
    url="https://github.com/AceofSpades5757/clip-util",
    project_urls={
        "Documentation": "https://clip-util.readthedocs.io/en/latest/",
        "Author": "https://github.com/AceofSpades5757",
    },
    description="Clipboard utilities for use with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.9",
    packages=["clipboard"],
    package_dir={"": "src"},
    extras_require={
        "dev": dev_requires,
        "build": build_requires,
        "test": test_requires,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
