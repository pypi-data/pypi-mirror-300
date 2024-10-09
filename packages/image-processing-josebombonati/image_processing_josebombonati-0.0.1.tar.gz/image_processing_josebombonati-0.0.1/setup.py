from setuptools import setup, find_packages

with open ('README.md', 'r') as f:
    page_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name = 'image_processing_josebombonati',
    version = '0.0.1',
    author = 'jose bombonati',
    description = 'Com o pacote image-processing, você poderá realizar transformações incríveis em suas imagens',
    long_description = page_description,
    long_description_content_type = 'text/markdown',
    url =  'https://github.com/juniorbombonati/image-processing-package',
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.5'
)

