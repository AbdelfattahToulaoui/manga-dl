#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='manga-dl',
        version='0.1',
        description="A collection of scrapers to download manga",
        author='Abdelfattah Toulaoui',
        entry_points= {
            'console_scripts': [
                'manga-dl = manga_dl.__main__:main'
                ]
            },
        packages = find_packages(),
        install_requires=[
            'bs4',
            'requests',
            'pyexecjs'
      )
