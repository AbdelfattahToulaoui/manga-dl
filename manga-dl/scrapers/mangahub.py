from .downloader import Downloader
from .title import Title
from .sweeper import Sweeper
import requests
from bs4 import BeautifulSoup
from .utils import *
import re


''' A scraper for https://mangahub.io/ '''

class MangahubDownloader(Downloader):
    def __init__(self, url):
        Downloader.__init__(self, url)
        self._html = load_url(self.session, url)
        self.images = self.getImageURLs()
    
    def getImageURLs(self):
        soup = BeautifulSoup(self._html, 'html.parser')
        # Find the first image, we can build the rest from there
        src = soup.find("img", class_="PB0mN")['src']
        m = re.match('(.*/[^0-9]*)[0-9]*([^0-9/]*\..*)', src)
        # Find the total number of pages
        number = soup.find("p", class_="_3w1ww").text.split('/')
        minpage = int(number[0])
        maxpage = int(number[1])
        urls = []
        for i in range(minpage, maxpage+1):
            # Build a url now
            url = m.group(1) + str(i) + m.group(2)
            urls.append(url)
        return urls
    

class MangahubTitle(Title):
    def __init__(self, url):
        Title.__init__(self, url)
        self._html = load_url(self.session, url)
    
    def getChapterList(self, lang = None):
        ret = []
        soup = BeautifulSoup(self._html, 'html.parser')
        chapters = soup.findAll('a', class_='_2U6DJ')
        for ch in chapters:
            number = str_to_float(ch.find('span',
                                             class_='_3D1SJ').text[1:])
            title = ch.find('span', class_='_2IG5P').text
            link = ch['href']
            ret.append({
                'number': number,
                'title': title,
                'url' : link
            })
        return ret
        

class MangahubSweeper(Sweeper):
    
    def getMangaList(self):
        url = 'https://mangahub.io/search'
        for i in self._searchURL(url, True):
            yield i
    
    def searchManga(self, query):
        qquery = requests.utils.quote(query)
        url = 'https://mangahub.io/search?q=' + qquery
        return [i for i in self._searchURL(url)]
    
    def _searchURL(self, url, recursive=False):
        self.url = url
        cont = True
        while cont:
            self.pageEnd = False
            soup = bs_from_url(self.session, self.url)
            for i in self._searchPage(self.url):
                yield i
            self.pageEnd = True
            if recursive and next and next.has_attr('href'):
                try:
                    next = soup.find('li', class_='next').find('a')
                    self.url = next['href']
                except:
                    cont = False
            else:
                cont = False
    
    def _searchPage(self, url):
        soup = bs_from_url(self.session, url)
        mangas = soup.find('div', id='mangalist').findAll('div', class_='_1KYcM')
        for manga in mangas:
            img = manga.find('img', class_='manga-thumb')['src']
            a = manga.find('h4', 'media-heading').find('a')
            link = a['href']
            title = a.text
            yield {
                'title': title,
                'cover': img,
                'url': link 
            }
        

