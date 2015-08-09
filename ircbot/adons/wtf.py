# UrbanDictonary module adapted from
# https://github.com/EvilzoneLabs/BeastBot/blob/sqlite/src/inc/modules/urban.py
# This is a quick port, also going from Python2 to Python3, kinda hacked
# together. I remove some features like the voting on urbandictonary.

import urllib.request
import json
import sys

def urban(word):
    word = word.strip()
    # make it url friendly
    if " " in word:
        word = word.replace(" ", "%20")
    url = "http://api.urbandictionary.com/v0/define?term=" + word
    info = urllib.request.urlopen(url)
    try:
        data = json.loads(info.read().decode("utf-8"))
        definition = data["list"][0]["definition"].replace("\n", " ").replace("\r", "")
        output = word.replace("%20", " ") + ": " + definition
        return output
    except IndexError:
        return "No definition."
                
def main(nick, comargs, chan, send):
    w = comargs.strip()
    define = urban(w)
    send.put(define)
