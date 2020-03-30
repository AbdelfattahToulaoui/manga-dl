import requests
import mimetypes
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
    
    def download(self, directory):
        ''' Download the images from the site
            to the specified directory
            
            :param directory: a directory to download pages to
        '''
        for index, img in enumerate(self.images):
            yield (index, len(self.images))
            req = self.session.get(img)
            try:
                content_type = req.headers['Content-Type'].split(';')[0]
                ext = mimetypes.guess_extension(content_type)
            except:
                ext = ''
            
            path = os.path.join(directory, '%03i%s' % (index,ext))
            
            with open(path, 'wb') as output:
                output.write(req.content)
        yield (len(self.images), len(self.images)) 
