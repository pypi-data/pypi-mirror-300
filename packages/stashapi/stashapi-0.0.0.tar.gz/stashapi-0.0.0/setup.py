import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="stashapi",
    version="0.0.0",
    description="This is a dummy package designed to prevent namesquatting on PyPI. You should install stashapp-tools instead.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stg-annon/stashapp-tools",
    author="stg-annon",
    author_email="14135675+stg-annon@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["stashapi-dummy"],
    include_package_data=True,
    install_requires=["requests"],
)