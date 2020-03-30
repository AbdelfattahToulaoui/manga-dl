from .downloader import Downloader
from .title import Title
from .sweeper import Sweeper
from .utils import *
import re

''' Downloads manga from https://manganelo.com/ '''

# Manganelo is simple enough to scrape from

class ManganeloDownloader(Downloader):
    def __init__(self, url):
        Downloader.__init__(self, url)
        self._html = load_url(self.session, url)
        self.images = self.getImageURLs()
    
    def getImageURLs(self):
        soup = BeautifulSoup(self._html, 'html.parser')
        container = soup.find('div', class_="container-chapter-reader")
        return [ page['src'] for page in 
                container.findAll('img')]
        

class ManganeloTitle(Title):
    def __init__(self, url):
        Title.__init__(self, url)
        self._html = load_url(self.session, url)
        
    def getChapterList(self, lang = None):
        ret = []
        soup = BeautifulSoup(self._html, 'html.parser')
        container = soup.find('ul', class_='row-content-chapter')
        for chapter in container.findAll('a', class_='chapter-name'):
            title = chapter.text
            link = chapter['href']
            m = re.search('Chapter ?([0-9\.]*)', title)
            if m and m.group(1).isdecimal():
                number = str_to_float(m.group(1))
            else:
                number = 0
            ret.append({
                'number': number,
                'title': title,
                'url' : link
            })
        return ret

class ManganeloSweeper(Sweeper):
    
    def getMangaList(self):
        cont = True
        page = 1
        while cont:
            self.pageEnd = False
            url = 'https://manganelo.com/genre-all/' + str(page)
            soup = bs_from_url(self.session, url)
            mangas = soup.findAll('div', class_='content-genres-item')
            if url == soup.find('a', class_='page-last')['href']:
                break
            for manga in mangas:
                self.pageEnd = False
                img = manga.find('img', class_='img-loading')['src']
                a = manga.find('a', 'genres-item-name')
                link = a['href']
                title = a.text
                yield {
                    'title': title,
                    'cover': img,
                    'url': link 
                }
            self.pageEnd = True
            page += 1
    
    def searchManga(self, query):
        qquery = re.sub('[^0-9a-zA-Z]+', '_', query)
        url = 'https://manganelo.com/search/' + qquery
        print(url)
        soup = bs_from_url(self.session, url)
        mangas = soup.findAll('div', class_='search-story-item')
        ret = []
        for manga in mangas:
            self.pageEnd = False
            img = manga.find('img', class_='img-loading')['src']
            a = manga.find('a', 'item-title')
            link = a['href']
            title = a.text
            ret.append({
                'title': title,
                'cover': img,
                'url': link 
            })
        return ret

 
