from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description=f.read()
with open('requirements.txt') as f:
    requirements=f.read().splitlines()
    
setup(
    name='coisado',
    version='0.0.1',
    author='Julio Rufino',
    author_email='jarufino@bol.com.br',
    description='Quero uma vaga homeoffice',
    long_description="sou um sonhador com aspiração a programador ou analista de suporte cloud (de preferência), aspirando um anywhareoffice/nômade digital. E claro, sem a ajuda do Senhro Jesus, não conseguirei",
    long_description_content_type='text/markdown',
    packages=find_packages(),
)