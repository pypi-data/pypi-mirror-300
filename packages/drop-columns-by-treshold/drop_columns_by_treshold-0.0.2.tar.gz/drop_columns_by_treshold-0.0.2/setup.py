import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "drop_columns_by_treshold",
    version = "0.0.2",
    author = "Ganbaatar Bold",
    author_email = "elmerganbaa@gmail.com",
    description = "drop_columns_by_treshold",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ganbaaelmer/drop_columns_by_treshold.git",
    project_urls = {
        "Bug Tracker": "https://github.com/ganbaaelmer/drop_columns_by_treshold.git",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)