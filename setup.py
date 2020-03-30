# 
# Copyright 2020 Abdelfattah Toulaoui
# 
# This file is part of Manga-DL.
# 
# Manga-DL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Manga-DL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Manga-DL.  If not, see <https://www.gnu.org/licenses/>. 


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
            ]
      )
