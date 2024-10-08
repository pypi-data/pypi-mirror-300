from setuptools import setup, find_packages
import os

# Função para incluir os arquivos .pyc na distribuição
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".pyc"):  # Incluir somente os arquivos .pyc
                paths.append(os.path.join(path, filename))
    return paths

# Caminho para incluir arquivos .pyc
pyc_files = package_files('jose_meu_pacote/__pycache__')

setup(
    name="jose_meu_pacote",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # Incluir dados como arquivos .pyc
     package_data={'jose_meu_pacote': ['*.pyc']},  # Incluir os arquivos .pyc
    description="Um pacote com bytecode compilado",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
