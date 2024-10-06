from setuptools import setup, find_packages

with open("README.md") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bank_python",
    version="0.0.2",
    author="Giovanna Sousa",
    author_email="19giihsousa@gmail.com",
    description="Um sistema bancário simples em Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eigiihs/bank_python_package",
    packages=find_packages(),
    install_requires=requirements
)