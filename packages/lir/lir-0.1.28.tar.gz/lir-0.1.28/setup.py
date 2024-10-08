from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()
setup(
    name="lir",
    version="0.1.28",
    description="scripts for calculating likelihood ratios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NetherlandsForensicInstitute/lir",
    author="Netherlands Forensic Institute",
    author_email="fbda@nfi.nl",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "scikit-learn>=1.4",
        "tqdm",
        "pandas",
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
