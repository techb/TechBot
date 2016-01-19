
import json
import urllib.request

def getMovieInfo(title):
    titlesplit = title.lower().strip().split() #oh may lol
    # if the movie title is more than one word,
    # join it so the url can use it, else just nothing
    if len(titlesplit) > 1:
        newtitle = "+".join(titlesplit)
    else:
        newtitle = titlesplit[0]

    url = "http://www.omdbapi.com/?t=%s&plot=short&r=json" % newtitle
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    if data['Response'] == 'True':
        return (data['Title'],
                data['Year'],
                data['imdbRating'],
                data['Plot'],
                data['imdbID')
    else:
        return (False, "Movie: %s not found, check spelling?" % title)

def main(nick, comargs, chan, send):
    data = getMovieInfo(comargs)
    if data[0] != False:
        send.put(("%s: Year: %s IMDB: %s Plot: %s" % (data[0], data[1], data[2], data[3]), chan))
        send.put(("http://www.imdb.com/title/tt2294629/%s/" %data[4], chan)
    else:
        send.put((data[1], chan))
