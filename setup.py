from setuptools import setup, find_packages

setup(
    name="orthofetch",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'click',
        'rich',
        'aiohttp',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'orthofetch=orthofetch.main:main',
        ],
    },
)