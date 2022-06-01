from setuptools import find_packages, setup

setup(
    name='IG_Scraper',
    packages=find_packages(include=['data', 'scripts', 'src']),
    version='0.0.1',
    description='Instagram scraping tool',
    author='Alessandro Togni',
    license='MIT',
    python_requires='>=3'
)