import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kelian",
    version="0.1.3",
    author="Kelian",
    description="Bibliothèque de bouts de code utiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Game-K-Hack/kelian",
    project_urls={
        "Bug Tracker": "https://github.com/Game-K-Hack/kelian/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11",
    install_requires=[
        "pywin32", 
        "WMI"
    ]
)
