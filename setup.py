from setuptools import setup, find_packages

setup(
    name="orthofetch",
    version="0.2",
    description="Orthodox Christian system fetch tool",
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["orthofetch", "orthofetch.*"]),
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
    package_data={
        'orthofetch': ['logos/*.txt'],
    },
)