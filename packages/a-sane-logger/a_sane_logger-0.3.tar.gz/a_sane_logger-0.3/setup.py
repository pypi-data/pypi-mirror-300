# setup.py
from setuptools import setup, find_packages

setup(
    name='a_sane_logger',  # Updated module name
    version='0.3',
    author='Alex Popescu',
    author_email='pop.alx@gmail.com',
    description='A simple logging configuration module',
    keywords='logging',
    # packages=find_packages(),
    packages=['a_sane_logger'],
    include_package_data=True,
    zip_safe=True,
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description_content_type="text/markdown", 
    long_description=open('README.md').read(),
)
