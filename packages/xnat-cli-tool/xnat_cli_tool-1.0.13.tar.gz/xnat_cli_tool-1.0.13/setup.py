from setuptools import setup, find_packages
import os

def read_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(
    name='xnat_cli_tool',
    version='1.0.13',
    author='Amr Shadid',
    author_email='amr.shadid@nyu.edu',
    description='XNAT CLI Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amrshadid/xnat_cli_tool',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'xt=cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
