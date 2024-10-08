from setuptools import setup

setup(
    name='wiki_synonyms',
    version='0.3.0',
    description='Python package for Wiki synonyms',
    url='https://github.com/iis-research-team/wiki-synonyms',
    author='IIS Research Team',
    author_email='bruches@bk.ru',
    license='MIT',
    packages=['src'],
    install_requires=[
                      'numpy',
                      ],
)
