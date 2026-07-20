from pathlib import Path

from setuptools import find_packages, setup


requirements_file = Path(__file__).with_name("requirements.txt")
install_requires = [
    requirement.strip()
    for requirement in requirements_file.read_text(encoding="utf-8").splitlines()
    if requirement.strip() and not requirement.lstrip().startswith("#")
]

setup(
    name="red_statutory",
    version="0.0.1",
    description="RED Statutory Register Generator",
    author="REDANCHOR",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
