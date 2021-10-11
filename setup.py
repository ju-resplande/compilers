from setuptools import setup, find_packages

setup(
    name="mgol",  # Required
    version="1.0.0",  # Required
    description="Compiler for mgol",  # Optional
    url="https://github.com/jubs12/compilers",
    author="Juliana Resplande",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Natural Language :: Portuguese",
        "Programming Language :: Python :: 3.7",
        "Topic :: Education",
        "Topic :: Software Development :: Compilers",
    ],
    keywords="mgol, compilers, educational software",  # Optional
    package_dir={"": "src"},  # Optional
    install_requires=["pandas",],
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7",
)

