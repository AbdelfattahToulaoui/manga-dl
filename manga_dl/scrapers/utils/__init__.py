from bs4 import BeautifulSoup

# Headers to be used when we want to disguise
# the user agent
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
            }

def load_url(session, url, params=None, headers=None):
    req = session.get(url, params=params, headers=headers)
    if req.ok:
        return req.text
    else:
        raise Exception("Request returned non 200 status") 

def bs_from_url(session, url, params=None):
    return BeautifulSoup(load_url(session, url, params), 'html.parser')

def str_to_float(s):
    if s.isdecimal():
        return float(s)
    else:
        return 0
