# my_package/setup.py
from setuptools import setup, find_packages

setup(
    name='dlibex',
    version='1.11',
    packages=find_packages(),
    description='This library is used for malware development. For educational purposes only!',
    author='Anthony',
    author_email='anthonyadams9821@gmail.com',
    url='',
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
