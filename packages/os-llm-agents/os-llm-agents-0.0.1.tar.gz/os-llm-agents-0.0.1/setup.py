import os
import setuptools


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements():
    """
    Reads the requirements.txt file
    """
    reqs_path = os.path.join(__location__, 'requirements.txt')
    with open(reqs_path, encoding='utf8') as f:
        reqs = [line.strip() for line in f if not line.strip().startswith('#')]

    names = []
    for req in reqs:
        names.append(req)
    return {'install_requires': names}


setuptools.setup(
    name="os-llm-agents",
    version="0.0.1",
    author="Aleksandr Perevalov, Andreas Both",
    author_email="aleksandr.perevalov@htwk-leipzig.de,andreas.both@htwk-leipzig.de",
    description="Python package that helps to build LLM agents based on open-source models from Huggingface Hub.",
    long_description=long_description,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/WSE-research/open-source-llm-agents",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    packages=setuptools.find_packages(),
    keywords="llm agents huggingface transformers",
    **read_requirements()
)