from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_ottojacometo",
    version="0.0.1",
    author="Otto-21",
    author_email="otto.jacometo@gmail.com",
    description="Realiza o processamento de imagens (combinação e transformação).",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Otto-21/image_processing_package.git",
    packages= find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)