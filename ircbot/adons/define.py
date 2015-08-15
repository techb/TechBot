import urllib
import urllib.request
import bs4
from bs4 import BeautifulSoup

def define(word):
    rs = ''
    url = "http://dictionary.reference.com/browse/" + word
    try:
        info = urllib.request.urlopen(url)
        soup = BeautifulSoup(info.read(), "lxml")
        defset = soup.find_all("div", class_="def-content")
        # in case there is link tag in the def, we just grab the text
        for c in defset[0].contents:
            if type(c) == bs4.element.Tag:
                rs += c.get_text()
            else:
                rs += c

        if defset:
            out = "Def: %s" % rs.strip() # strip() incase of prepended or tailing \n
            more = "More on %s found: %s" % (word, url)
            return([out, more])
            
    except urllib.error.HTTPError as e:
        return "404 word not found"
        
def main(nick, comargs, chan, send):
    comargs = comargs.strip()
    data = define(comargs)
    send.put((nick, chan, data))
    
