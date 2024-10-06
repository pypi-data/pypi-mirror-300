from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='pguid',
    version='0.0.6',
    packages=find_packages(),
    install_requires=[
        'pygame>=1.9.1'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)