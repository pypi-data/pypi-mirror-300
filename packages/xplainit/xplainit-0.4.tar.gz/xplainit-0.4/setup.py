from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xplainit',
    version='0.4', 
    description='A library to generate natural language explanations of ML model predictions',
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    author='Leandre Nash',
    author_email='leandrework@gmail.com',
    url='https://github.com/',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'matplotlib',
    ],
    license='MIT',  
)


