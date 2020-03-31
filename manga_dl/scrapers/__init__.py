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


from .mangadex  import *
from .mangafox  import *
from .mangahub  import *
from .manganelo import *
import math
import os
import shutil
import re
import tempfile
import sys

def _float(f):
    return ('%f' % f).rstrip('0').rstrip('.')

class Scraper:
    ''' A class to scrape data from manga sites
        using the site specific scrapers
    '''
    def getScraper(site):
        ''' A class method to get the scrapers
            of a site from the available scrapers
            
            :param site: The name of website to use
        '''
        if site in scrapers:
            return Scraper(*scrapers[site])
        else:
            raise Exception('Unsupported scraper')
        
    def __init__(self, downloader, title, sweeper):
        ''' Initialize the class with downloader, tilte, and sweeper
            classes it needs to function
        '''
        self.downloader = downloader
        self.title = title
        self.sweeper = sweeper
    
    def downloadChapters(self, manga, chapter_list=[], begin_ch=-1, end_ch=-1, directory='.', lang=None, manga_search_index=0, cbz=False):
        ''' Downloads the chapters in the range specified for a manga
        
            :param manga: a search term to use to look for the title
            :param chapters: a list of chapters to download
            :param begin_ch: the first chapter in the range
            :param end_ch: the last chapter in the range
            :param directory: The directory to download the manga to
            :param lang: for multilingual sites, this specifies which language to look for
            :param manga_search_index: look for the nth ranked result in the search
            :param cbz: create a cbz if true, a simple directory if false
        '''
        sweeper = self.sweeper()
        mangas = sweeper.searchManga(manga)
        
        try:
            manga = mangas[manga_search_index]
        except IndexError:
            print('Manga not found', file=sys.stderr)
            sys.exit(1)
        
        print('Found manga: %s' % manga['title'])
        
        title = self.title(manga['url'])
        
        # Check if using a range or a chapter list
        if not chapter_list:
            chapters = title.getChapterRange(begin_ch, end_ch
                                        if end_ch!=-1 else math.inf, lang=lang)
        else:
            chapters = [ ch for ch in title.getChapterList(lang=lang)
                        if ch['number'] in chapter_list]
        if not chapters:
            print('No chapters found', file=sys.stderr)
            sys.exit(1)
        
        # Check for missing chapters
        numbers = [ch['number'] for ch in chapters]
        missing = [ch for ch in chapter_list if ch not in numbers]
        if missing:
            print('Chapter(s) %s not found' % str.join(',', map(_float, missing))
                                                       , file=sys.stderr)
            sys.exit(1)
        
        # Sort the chapters before downloading
        chapters.sort(key=lambda ch: ch['number'])
        
        for ch in chapters:
            downloader = self.downloader(ch['url'])
            path = os.path.join(
                    directory,
                    manga['title'],
                    ch['title']
                    )
            # This won't be necessary in the case of a CBZ file
            # but I use it to confirm that the path is writeable
            # and that it's not against the rules of the OS
            try:
                os.makedirs(path)
            except:
                # Try escaping the path, if it still doesn't work
                # throw and error
                try:
                    path = re.sub('\<|\>|\:|\"|\||\?\*', '_', path)
                except:
                    raise Exception('Cannot create directory ' + path)
            print('Downloading chapter: %s' % _float(ch['number']), end='')
            if 'lang' in ch:
                print('(%s)' % ch['lang'])
            print()
            # Create a temporary directory to store the images
            try:
                # Finally download
                for state in downloader.download(path):
                    print('Downloading %i/%i'%state, end='\r')
            except:
                # In case of an error don't create a cbz, just copy the files
                print()
                print('Encountered an error', file=sys.stderr)
                cbz = False
            print()
            if cbz:
                print('Packing the CBZ file...')
                # Remove any trailing slashes
                zfile = re.sub('(\\|/)*$', '', path)
                # Create a zip file
                shutil.make_archive(zfile,
                                    format = 'zip',
                                    base_dir='.',
                                    root_dir=path)
                # Rename the .zip to a .cbz
                shutil.move(zfile + '.zip', zfile + '.cbz')
                # Remove the path
                shutil.rmtree(path, ignore_errors=True)
                print('Created CBZ file')
                
    def listChapters(self, manga, lang=None, manga_search_index=0):
            ''' List chapters in the the manga
            
                :param manga: a search term to use to look for the title
                :param lang: for multilingual sites, this specifies which language to look for
                :param manga_search_index: look for the nth ranked result in the search
            '''
            sweeper = self.sweeper()
            mangas = sweeper.searchManga(manga)
            
            try:
                manga = mangas[manga_search_index]
            except IndexError:
                print('Manga no found' ,file=sys.stderr)
                sys.exit(1)
            
            title = self.title(manga['url'])
            for ch in title.getChapterList(lang=lang):
                print("%s" % _float(ch['number']), end='')
                if 'lang' in ch:
                    print("(%s)" % ch['lang'], end='')
                print(": %s" % ch['title'])
    
    def listMangas(self, search=None):
            ''' Mangas on the site
            
                :param search: a search term to use to look for the title, if not present it will list all mangas in the site
            '''
            sweeper = self.sweeper()
            if not search:
                print('Fetching all manga on the site, this may take a while...')
                mangas = [i for i in sweeper.getMangaList()]
            else:
                mangas = sweeper.searchManga(search)
            
            for index, manga in enumerate(mangas):
                print("%02d: %s" % (index, manga['title']))

# The available scrapers
scrapers = {
        'mangadex': (MangadexDownloader,
                     MangadexTitle,
                     MangadexSweeper),
        
        'mangafox': (MangafoxDownloader,
                     MangafoxTitle,
                     MangafoxSweeper),
        
        'mangahub': (MangahubDownloader,
                     MangahubTitle,
                     MangahubSweeper),
        
        'mangakakalot': (ManganeloDownloader,
                         ManganeloTitle,
                         ManganeloSweeper),
        
        'manganelo': (ManganeloDownloader,
                      ManganeloTitle,
                      ManganeloSweeper),
}

