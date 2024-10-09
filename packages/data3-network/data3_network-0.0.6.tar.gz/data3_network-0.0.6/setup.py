from setuptools import setup, find_packages

setup(
    name='data3_network',
    version='0.0.6',
    packages=find_packages(),
    install_requires=[
        "pymongo==4.6.3",
    ],
    author='Data3 Network',
    author_email='data3network@gmail.com',
    description='Data3 Network Library for Data Access',
)


