from setuptools import find_packages, setup


setup(
    name="red_statutory",
    version="0.0.1",
    description="RED Statutory Register Generator",
    author="REDANCHOR",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["frappe"],
)
