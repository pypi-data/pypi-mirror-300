from setuptools import setup, find_packages

setup(
    name='utilitario_de_leitura_de_arquivos_csv',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Adicione suas dependências aqui

    ],
    author='Silvio',
    author_email='lerparaaprendersempre@gmail.com',
    description='Um pacote que fornece funções para ler arquivos CSV e retornar dados como listas ou dicionários.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/silvioprogramation22/Utilitario_de_Leitura_de_Arquivos_CSV',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
