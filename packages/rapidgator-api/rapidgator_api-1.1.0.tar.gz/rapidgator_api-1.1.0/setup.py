from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='rapidgator_api',
    version='1.1.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Python client library for the Rapidgator API',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
    ],
    author='Zack3D',
    author_email='zack3d@goocat.gay',
    url='https://git.goocat.gay',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
