from setuptools import setup, find_packages

setup(
    name='xplainit',
    version='0.1',
    description='A library to generate natural language explanations of ML model predictions',
    author='Leandre Nash',
    author_email='leandrework@gmail.com',
    url='https://github.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'matplotlib',
    ],
)
