from setuptools import setup, find_packages

setup(
    name='minidb_project',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # Adicione aqui as dependências necessárias
    ],
    description='Uma biblioteca de banco de dados simples que funciona a partir do script',
    long_description=open('README.md').read(),  # Certifique-se de que você tem um README.md
    long_description_content_type='text/markdown',  # Formato do README
    author='Arthur Saert',
    author_email='contato@grupomuller.org.br',
    url='https://grupomuller.org.br',  # URL do repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # ou a licença que você escolher
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)