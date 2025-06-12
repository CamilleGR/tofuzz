from setuptools import setup, find_packages

setup(
    name='tofuzz',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
        'requests[socks]'
    ],
    entry_points={
        'console_scripts': [
            'tofuzz = tofuzz.cli:cli'
        ]
    },
)