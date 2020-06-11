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
import mimetypes
import concurrent.futures
import os
from abc import ABC

class Downloader(ABC):
    ''' An class to download a chapter from a website ''' 
    def __init__(self, url):
        ''' Initialize the object with a url.'''
        self.session = requests.Session()
        self.url = url
        self.images = []
    
    def getImageURLs(self):
        ''' Gets the urls of Images from the site
            returns a list of url strings
            
            :returns: a list of strings representing urls
        '''
        raise NotImplementedError()
    
    def download(self, directory, ondone=None):
        ''' Download the images from the site
            to the specified directory
            
            :param directory: a directory to download pages to
        '''
        self._downloaded = 0
        def di(url, done):
            self.download_img(url, directory, done)
            self._downloaded += 1
            if(ondone):
                ondone(self._downloaded, len(self.images))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i in range(len(self.images)):
                executor.submit(di, self.images[i], i)


    def download_img(self, url, directory, index):
        req = self.session.get(url)
        try:
            content_type = req.headers['Content-Type'].split(';')[0]
            ext = mimetypes.guess_extension(content_type)
            # though technically the same, jpe is less popular that jpg
            if ext=='.jpe':
                ext = '.jpg'
        except:
            ext = ''
        path = os.path.join(directory, '%03i%s' % (index,ext))
        with open(path, 'wb') as output:
            output.write(req.content)
