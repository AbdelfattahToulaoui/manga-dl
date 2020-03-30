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
