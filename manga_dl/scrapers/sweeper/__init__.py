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


import requests
from abc import ABC

class Sweeper(ABC):
    def __init__(self):
        ''' An abstract class to sweep a website for
            available titles
        '''
        self.session = requests.Session()
        self.pageEnd = False
    
    def getMangaList(self):
        ''' Gets a list of all manga on the site
            it is done in the form of a generator
            to prevent potential useless loading
            since most sites paginate their output.
            returns a list of dict with as follows:
            {title: The title of the manga,
            cover: The link to cover image or None,
            url: The url of the manga}
            
            :returns: a generator dicts of manga titles
        '''
        raise NotImplementedError()
    
    def searchManga(self, query):
        ''' Searches the site for a specific query
            with the same return format as getMangaList()
            
            :returns: a list dicts of manga titles
        '''
        raise NotImplementedError()
