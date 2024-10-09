from setuptools import setup, find_packages

setup(
    name='gsession',
    version='0.1.4',
    description='Un package pour gerer les session de 42',
    author='guiguito',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'gsession = gsession.main:main',
        ],
    },
)
