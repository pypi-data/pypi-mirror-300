# pylint: disable=missing-module-docstring
from setuptools import setup, find_packages

setup(
    name='dexipy',
    version='1.0.0',
    description='A software package for using DEXi models in Python',
    author='Marko Bohanec',
    author_email='marko.bohanec@ijs.si',
    keywords="Decision EXpert, DEX method, multi-criteria, decision model, MCDM",
    #packages=['dexipy',],
    packages=find_packages(),
    url='https://repo.ijs.si/markobohanec/dexipy',
    license='LICENSE.md',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7, <4",
    install_requires=[
        'matplotlib'
    ],
    project_urls={
        "Source": "https://repo.ijs.si/markobohanec/dexipy",
        "Documentation": "https://dex.ijs.si/documentation/DEXiPy/",
    },
)
