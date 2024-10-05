import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appartme_paas",
    version="0.1.0",
    author="Miłosz Dębiński",
    author_email="milosz.debinski@appartme.com",
    description="Python client library for Appartme PaaS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MiloszSlabs/appartme_paas_python",
    project_urls={
        "Bug Tracker": "https://github.com/MiloszSlabs/appartme_paas_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.7.4,<4.0.0",
    ],
)