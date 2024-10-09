# setup.py
import os
from setuptools import setup, find_packages

# Get the absolute path to the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Read README.md file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Reads the requirements.txt file
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='appeears-api-client',
    version='0.1.3',
    packages=find_packages(),
    license='MIT',
    description='Python client for interacting with NASA Earthdata\'s AppEEARS API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Francisco Furey',
    author_email='franciscofurey@gmail.com',
    url='https://github.com/franfurey/appeears_api_pip_package',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.7',
)
