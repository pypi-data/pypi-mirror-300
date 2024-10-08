from setuptools import setup, find_packages

setup(
    name="ctkmessagebox2",  # Nome do pacote que será usado para instalar via pip
    version="0.1.0",  # Versão inicial do pacote
    packages=find_packages(),  # Localiza todos os pacotes Python dentro do diretório
    include_package_data=True,  # Inclui arquivos como ícones (definidos em MANIFEST.in)
    description="The MessageBox package for CustomTkinter",
    long_description=open('README.md').read(),  # Lê o README.md como descrição longa
    long_description_content_type="text/markdown",  # Tipo de conteúdo do README
    author="Lucas Hoffman",
    author_email="hoffmanlucas@gmail.com",
    url="https://github.com/hoffmanlucas/ctkmessagebox.git",  # URL do seu repositório GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Versão mínima do Python
    install_requires=[  # Dependências do pacote, se houver
        "customtkinter",
        "Pillow"
    ],
)
