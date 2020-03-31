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
        # There are basically two variants of MangaFox
        # pages, distinguish them
        # My OCD is killing me over this line
        if(self._html.find("function(p,a,c,k,e,d){e=function(c){return(c<a?\"\":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p;}")) != -1:
            return self._getImageURLsV1()
        else:
            return self._getImageURLsV2()
    
    def _getImageURLsV2(self):
        function = re.compile("eval\((" + re.escape("function(p,a,c,k,e,d){e=function(c){return(c<a?\"\":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p;}") + ".*)\)")
        array = re.compile("var newImgs=([^;]+);")
        
        # Look for the target function
        fn = function.search(self._html).group(1)
        # Take the function, AND EVALUATE IT!
        arrstr = execjs.eval(fn)
        arrstr = array.search(arrstr).group(1)
        # Get the array
        arr = execjs.eval(arrstr)
        urls = []
        for i in arr:
            url = 'https:' + i
            if not url in urls:
                urls.append(url)
        return urls
    
    def _getImageURLsV1(self):
        # Define some regex for later use
        chapterid = re.compile('chapterid =([0-9]+);')
        pix = re.compile('var pix="([^"]*)";')
        pvalue = re.compile('pvalue=([^;]*);')
        # This is the class of the pager
        pager_class = "cp-pager-list"
        # Get the chapter id using the regex
        cid = chapterid.search(self._html).group(1)
        
        # Get all page links
        soup = BeautifulSoup(self._html, 'html.parser')
        pager = soup.find('div', class_=pager_class)
        if pager:
            pager = pager.find('span')
        else:
            return []
        # Get the page numbers in them
        pages = [int(a.text)
                 for a in pager.findAll("a") if a.text.isdigit()]
        # Get the minimum and maximum
        minpage = min(pages)
        maxpage = max(pages)
        urls = []
        for i in range(minpage, maxpage):
            # Download page container scripts from mangafox
            payload = {
                'cid': cid,
                'page': i,
                'key': ''
                }
            t = load_url(self.session, self.url + "/chapterfun.ashx", params=payload,
                         headers = {'X-Requested-With': 'XMLHttpRequest',
                                        'Sec-Fetch-Site': 'same-origin',
                                        'Referer': self.url})[5:-2]
            # Evaluate the obfuscated javascript within and
            # apply a regex to get the urls
            data = execjs.eval(t)
            pixdata = pix.search(data).group(1)
            data = execjs.eval(pvalue.search(data).group(1))
            # Add urls to the set
            for img in data:
                url = 'https:' + pixdata + img
                if not url in urls:
                    urls.append(url)
        return urls

class MangafoxTitle(Title):
    def __init__(self, url):
        Title.__init__(self, url)
        self.session.headers.update(headers)
        self._html = load_url(self.session, url)
    
    def getChapterList(self, lang = None):
        ret = []
        soup = BeautifulSoup(self._html, 'html.parser')
        chapterlist = soup.find('div', id='chapterlist')
        if not chapterlist:
            return []
        for chapter in chapterlist.findAll('li'):
            a = chapter.find('a')
            link = 'https://fanfox.net' + a['href']
            title = a.find('p', class_='title3').text
            number = str_to_float(re.search(
                'Ch\.([0-9\.]*)', title).group(1))
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
        self.url = 'https://fanfox.net/directory/'
        cont = True
        while cont:
            self.pageEnd = False
            soup = bs_from_url(self.session, self.url)
            for i in self._listFromSoup(soup, 'manga-list-1'):
                yield i
            self.pageEnd = True
            next = soup.find('a', text='>')
            if next and next.has_attr('href'):
                self.url = 'https://fanfox.net' + next['href']
            else:
                cont = False
    
    def searchManga(self, query):
        qquery = requests.utils.quote(query).replace('%20', '+')
        url = "https://fanfox.net/search?title=" + qquery
        soup = bs_from_url(self.session, url)
        return [i for i in self._listFromSoup(soup, 'manga-list-4')]
    
    def _listFromSoup(self, soup, prefix):
        # Since the search and global list pages
        # are similar with only different prefixes
        # for their classes, I grouped them together
        mangas = soup.find('div', class_=prefix)
        if not mangas:
            return []
        else:
            mangas = mangas.findAll('li')
        for manga in mangas:
            img = manga.find('img', class_=prefix + '-cover')['src']
            a = manga.find('p', prefix + '-item-title').find('a')
            link = 'https://fanfox.net' + a['href']
            title = a.text
            yield {
                'title': title,
                'cover': img,
                'url': link 
            }


