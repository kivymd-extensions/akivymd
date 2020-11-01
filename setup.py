import os
import re

from setuptools import find_packages, setup

extension_name = "akivymd"
package_name = "kivymd_extensions." + extension_name


def get_version() -> str:
    """Get __version__ from __init__.py file."""
    version_file = os.path.join(
        os.path.dirname(__file__),
        "kivymd_extensions",
        extension_name,
        "__init__.py",
    )
    version_file_data = open(version_file, "rt", encoding="utf-8").read()
    version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
    try:
        version = re.findall(version_regex, version_file_data, re.M)[0]
        return version
    except IndexError:
        raise ValueError(f"Unable to find version string in {version_file}.")


if __name__ == "__main__":
    # Static strings are in setup.cfg
    setup(
        name=package_name,
        description="A set of fancy widgets for KivyMD",
        version=get_version(),
        packages=(
            ["kivymd_extensions"]
            + find_packages(include=[package_name, package_name + ".*"])
        ),
        package_data={package_name: []},
        extras_require={
            "dev": [
                "pre-commit",
                "black",
                "isort[pyproject]",
                "flake8",
                "pytest",
                "pytest-cov",
                "pytest_asyncio",
                "pytest-timeout",
                "coveralls",
            ],
            "docs": [
                "sphinx",
                "sphinx-autoapi==1.4.0",
                "sphinx_rtd_theme",
            ],
        },
        install_requires=["kivymd>=0.104.1", "kivy>=1.11.1"],
        setup_requires=[],
        python_requires=">=3.6",
    )
