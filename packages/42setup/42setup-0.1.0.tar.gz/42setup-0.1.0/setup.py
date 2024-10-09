from setuptools import setup, find_packages

setup(
    name='42setup',
    version='0.1.0',
    description='Un package pour gerer les session de 42',
    author='guiguito',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'gsession = 42setup.main:main',
        ],
    },
)
