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
from .utils import *
import requests
from bs4 import BeautifulSoup
import re
import execjs

''' A scraper for https://fanfox.net/ '''

class MangafoxDownloader(Downloader):
    def __init__(self, url):
        Downloader.__init__(self, url)
        # Some headers to make the mangafox server believe we are using a browser
        self.session.headers.update(headers)
        self._html = load_url(self.session, url)
        self.images = self.getImageURLs()
    
    def getImageURLs(self):
        soup = BeautifulSoup(self._html, 'html.parser')
        pages = soup.find('select', class_='mangaread-page')
        imgs = []
        for page in pages.findAll('option'):
            s = bs_from_url(self.session, 'https:' + page['value'])
            imgs.append(s.find('img', id='image')['src'])
        return imgs

class MangafoxTitle(Title):
    def __init__(self, url):
        Title.__init__(self, url)
        self.session.headers.update(headers)
        self._html = load_url(self.session, url)
    
    def getChapterList(self, lang = None):
        ret = []
        soup = BeautifulSoup(self._html, 'html.parser')
        chapterlist = soup.find('div', class_='manga-chapters')
        if not chapterlist:
            return []
        for chapter in chapterlist.findAll('a'):
            link = 'https:' + chapter['href']
            title = re.sub('(^[\W]*)|([\W]*$)' , '', chapter.next)
            title = title.replace('\n', ' ')
            number = str_to_float(re.search(
                'Ch ([0-9\.]*)', title).group(1))
            ret.append({
                'number': number,
                'title': title,
                'url' : link
            })
        return ret

class MangafoxSweeper(Sweeper):
    def __init__(self):
        Sweeper.__init__(self)
        self.session.headers.update(headers)
    
    def getMangaList(self):
        self.url = 'https://m.fanfox.net/search/cate/all'
        cont = True
        while cont:
            self.pageEnd = False
            soup = bs_from_url(self.session, self.url)
            for i in self._listFromSoup(soup):
                yield i
            self.pageEnd = True
            next = soup.find('a', class_='next')
            if next and next.has_attr('href'):
                self.url = next['href']
            else:
                cont = False
    
    def searchManga(self, query):
        qquery = requests.utils.quote(query).replace('%20', '+')
        url = "https://m.fanfox.net/search?k=" + qquery
        soup = bs_from_url(self.session, url)
        ret = []
        return [i for i in self._listFromSoup(soup)]
    
    def _listFromSoup(self, soup):
        # Since the search and global list pages
        # are similar with only different prefixes
        # for their classes, I grouped them together
        mangas = soup.find('ul', class_='post-list')
        if not mangas:
            return []
        else:
            mangas = mangas.findAll('div', class_='post-one')
        for manga in mangas:
            img = manga.find('img')['src']
            title = manga.find('p', class_='title').text
            link = manga.find('a')['href']
            yield {
                'title': title,
                'cover': img,
                'url': link 
            }


