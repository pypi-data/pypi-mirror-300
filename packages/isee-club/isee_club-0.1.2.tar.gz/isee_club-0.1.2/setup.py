# setup.py

from setuptools import setup, find_packages

setup(
    name='isee_club',
    version='0.1.2',
    packages=find_packages(),
    description='isee club is public library',
    author='isee',
    author_email='',
    url='',  # GitHub 链接
    install_requires=[
        'pytz==2024.2',
    ],
)
