from setuptools import setup, find_packages

# Leer el contenido del archivo README.md"
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Shack4u",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[],
    author="Saul Villarreal",
    description="Una biblioteca para consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://Shack4u.io",
)
