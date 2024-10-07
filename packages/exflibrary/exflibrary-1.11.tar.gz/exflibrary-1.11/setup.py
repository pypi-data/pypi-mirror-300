# my_package/setup.py
from setuptools import setup, find_packages

setup(
    name='exflibrary',
    version='1.11',
    packages=find_packages(),
    description='Library for malware building, educational purposes only',
    author='Adam Johns',
    author_email='rusty128944@gmail.com',
    url='https://github.com/miracledevelop/exflibrary',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
