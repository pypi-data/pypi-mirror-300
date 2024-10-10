from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt",encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="coinverter",
    version="0.0.1",
    author="Pedro Arruda",
    author_email="pedrofelipega@gmail.com",
    description="Convesor de moedas com base do Real Brasileiro",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PedroFelipe-G-Arruda/coinverter",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)