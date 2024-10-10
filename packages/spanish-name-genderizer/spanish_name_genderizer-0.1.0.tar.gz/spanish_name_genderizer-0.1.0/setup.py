# setup.py

from setuptools import setup, find_packages

setup(
    name='spanish_name_genderizer',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'spanish_name_genderizer': ['data/*.csv']},
    install_requires=[
        'numpy>=1.26.4',
    ],
    author='Bakwenye Benjamin',
    author_email='benjamin.bakwenye@bse.eu',
    description='A library to genderize Spanish names',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/baksben/spanish_name_genderizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)