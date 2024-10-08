from setuptools import setup, find_packages

setup(
    name="itgpy",
    version="0.1.1",
    description="Integrated Toolkits for Gravity: A Python library for handling gravitational data and calculations.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Dongchan Kim",
    author_email="krq3268@cau.ac.kr",
    url="https://gitlab.com/nr-mini/itg",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.18.0",
        "matplotlib>=3.1.0",
        "scipy>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8",
            "black",
            "sphinx==7.3.7",
            "sphinx-rtd-theme==2.0.0",
            "sphinx-autodoc-typehints==2.3.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
