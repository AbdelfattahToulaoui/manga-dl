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

class Title(ABC):
    ''' A class representing a specific manga title. '''
    def __init__(self, url):
        ''' Initialize the title with a link.'''
        self.session = requests.Session()
        self.url = url
    
    def getChapterList(self, lang=None):
        ''' Gets a list of dictionaries of where the keys
            are the 'number' of the chapter, the
            'title' and 'url' with their respective values.
            For multi-lingual sites, the lang parameter specifies
            the language code to use, None will return all chapters.
            The number should always be a valid float, if not, it should
            be set to 0
            
            :param lang: language to download.
            :returns: a list of chapters.
        '''
        pass
    
    def getChapterRange(self, begin, end, lang=None):
        ''' Gets a range of chapters in the same
            format as getChapterList
            
            :param begin: the starting chapter
            :param end: the ending chapter.
            :param lang: language.
            :returns: A list of chapters
        '''
        ch = self.getChapterList(lang=lang)
        try:
            return [ k for k in ch 
                    if (
                        begin <= k['number'] <= end)
                    or (begin <= 0 and begin >= end) ]
        except KeyError:
            raise Exception('Invalid range')
