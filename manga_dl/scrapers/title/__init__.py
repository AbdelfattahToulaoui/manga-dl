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
                    if (k['number'].isdecimal() and
                        begin <= float(k['number']) <= end)
                    or (begin <= 0 and begin >= end) ]
        except KeyError:
            raise Exception('Invalid range')
