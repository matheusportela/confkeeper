from setuptools import setup

setup(
    name='confkeeper',
    version='0.0.1',
    packages=['confkeeper'],
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'confkeeper=confkeeper.confkeeper:cli'
        ]
    }
)