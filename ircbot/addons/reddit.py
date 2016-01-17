# reddit.py
# By: TechB
# praw is reddit api for python
#   pip3 install praw
# using python3


import praw
import itertools
import sys

import random
# seed from system time is fine
random.seed()

def reddit(subr):
    # don't put 'bot' in the name, else it will complain.
    reddit = praw.Reddit(user_agent="evilzone_techirc")
    try:
        # change the limit=100 to lower for quicker return times
        # BUT wont quarantee an image will be there
        hot = reddit.get_subreddit(subr, fetch=True).get_hot(limit=100)
    except:
        return("Subreddit not found...")

    choice = []
    for img in hot:
        iurl = img.url
        # get only formats we care about. .gif will also return .gifv
        if ".jpg" in iurl or ".png" in iurl or ".gif" in iurl:
            choice.append(iurl)

    if choice:
        # return some randome link from the '100' we found
        return(choice[random.randrange(0, len(choice))])
    else:
        return("No images")

def main(nick, comargs, chan, send):
    send.put((reddit(comargs), chan))
