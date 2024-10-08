from setuptools import setup, find_packages

setup(
    name='wiki_synonyms',
    version='0.3.7',
    description='Python package for Wiki synonyms',
    url='https://github.com/iis-research-team/wiki-synonyms',
    author='IIS Research Team',
    author_email='bruches@bk.ru',
    license='MIT',
    packages=find_packages(include=['wiki_synonyms', 'wiki_synonyms.*']),
    install_requires=[
                      'numpy',
                      ],
)
