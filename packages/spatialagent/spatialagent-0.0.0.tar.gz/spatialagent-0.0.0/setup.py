from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name='spatialagent',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'langchain==0.2.6',
        'scanpy[leiden]==1.10.2',
        'langchain-community==0.2.6',
        'tokencost==0.1.12',
        'cellxgene-census==1.14.1',
        'openai==1.35.4',
        'langchain-experimental==0.0.62',
        # "utag @ git+https://github.com/ElementoLab/utag.git@main",  # GitHub repo installation
        'liana==1.3.0',
        'langchain-openai==0.1.10',

    ],
    
    long_description=description,
    long_description_content_type='text/markdown',

)