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


from .downloader import Downloader
from .title import Title
from .sweeper import Sweeper
import requests
import json
from .utils import *
import re

''' A scraper for https://mangadex.org/ '''

# Mangadex makes things easier by employing an API
# through this API we get data in the form of json
# And parse it, but the API doesn't cover the list
# and search functions of the site

class MangadexDownloader(Downloader):
    def __init__(self, url):
        Downloader.__init__(self, url)
        self._data = json.loads(load_url(self.session, url))
        self.images = self.getImageURLs()
    
    def getImageURLs(self):
        server = self._data['server']
        hash = self._data['hash']
        pg_arr = self._data['page_array']
        ret = []
        for page in pg_arr:
            ret.append(server + hash + '/' + page)
        return ret

class MangadexTitle(Title):
    def __init__(self, url):
        Title.__init__(self, url)
        self._data = json.loads(load_url(self.session, url))
        
    def getChapterList(self, lang = None):
        ret = []
        for id, ch in self._data['chapter'].items():
            if lang != None and ch['lang_code'] != lang:
                continue
            
            title = ch['title']
            number = str_to_float(ch['chapter'])
            link = 'https://mangadex.org/api/chapter/' + id
            ret.append({
                'number': number,
                'lang': ch['lang_code'],
                'title': 'Ch.' + ch['chapter'] +
                '('+ch['lang_code']+')' + ' ' + title,
                'url' : link
            })
        return ret

class MangadexSweeper(Sweeper):
    def __init__(self):
        Sweeper.__init__(self)
        self.session.headers.update(headers)
    def getMangaList(self):
        cont = True
        page = 1
        while cont:
            self.pageEnd = False
            url = 'https://www.mangadex.org/titles/0/' + str(page)
            soup = bs_from_url(self.session, url)
            mangas = soup.findAll('div', class_='manga-entry')
            if not mangas:
                break
            for manga in mangas:
                self.pageEnd = False
                img = manga.find('div', class_='large_logo').find('img')['src']
                a = manga.find('a', 'manga_title')
                # Get the id of the manga
                id = re.search('/title/([0-9]+)/.*', a['href']).group(1)
                link = 'https://mangadex.org/api/manga/' +  id
                title = a.text
                yield {
                    'title': title,
                    'cover': img,
                    'url': link 
                }
            self.pageEnd = True
            page += 1
    
    def searchManga(self, query):
        # There is no way to search mangadex
        # without an account so, although I don't
        # like it, we'll have to enlist the help
        # of duckduckgo search to find it for us
        # PS: it might be slow to update, but it's
        # the only choice
        qquery = requests.utils.quote(query).replace('%20',
                    '+') + '+inurl%3A%27mangadex.org%2Ftitle%2F%27'
        soup = bs_from_url(self.session, 'https://duckduckgo.com/html/?q=' + qquery)
        ret = []
        for manga in soup.findAll('a', class_='result__a'):
            m = re.search('mangadex\.org/title/([0-9]*)/.*', manga['href'])
            if not m:
                continue
            id = m.group(1)
            title = re.search('^(.*?)( \(Title\) )?- MangaDex$', manga.text).group(1)
            link = 'https://mangadex.org/api/manga/' +  id
            img = 'https://mangadex.org/images/manga/%s.large.jpg' % id
            ret.append({
                    'title': title,
                    'cover': img,
                    'url': link 
            })
        return ret


