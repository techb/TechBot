#written for TechBot by techb

def main(nick, comargs, chan, send):
    '''does a /me with who/what ever is in comargs'''
    # example on sending a simple string to the default channel the bot is on
    send.put(("\001ACTION tips glass of beer with %s\001" % comargs, chan))
