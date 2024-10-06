from setuptools import setup, find_packages

setup(
    name="coolquote",  # Paket ismi
    version="0.1.0",  # Paket versiyonu
    author="efeecllk",
    author_email="efecelik576@gmail.com",
    description="A Python package that generates cool quotes based on different categories using a language model(GPT2).",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/efeecllk/coolquote",  #
    packages=find_packages(),  #
    install_requires=[
        "transformers",  # Hugging Face
        "torch"         #
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
