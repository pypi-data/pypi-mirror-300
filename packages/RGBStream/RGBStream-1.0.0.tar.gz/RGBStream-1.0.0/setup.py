from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='RGBStream',
    version='1.0.0',
    author='Prodigy0x',
    description='A Python package for Rainbow Text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://prodigy0x.netlify.app/',
    packages=find_packages(),
    python_requires='>=3.11',
)
