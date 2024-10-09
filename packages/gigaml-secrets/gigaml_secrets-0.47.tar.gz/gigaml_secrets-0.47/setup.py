from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gigaml_secrets',
    version='0.47',
    packages=find_packages(),
    install_requires=[
        'boto3',  # Add any other dependencies your package needs
        'botocore',
    ],
    author='Tautik Agrahari',
    author_email='tautik@gigaml.com',
    description='A library to manage AWS secrets with caching and environment variable integration',
    url='https://github.com/GigaML/GigaML-Secrets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='aws secrets manager caching environment variables',
    long_description=long_description,
    long_description_content_type='text/markdown',
)