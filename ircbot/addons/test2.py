import time
 
def main(nick, comargs, chan, q) :
    '''Look at irc.py -> sendIRC. It might changes, but till then
    this is how privmsg works or something, I am working on it, give me
    a day or two to make things clear.'''
    print(nick)
    print(chan)
    print(comargs)
    print("[*] Testing sending a private message not established")
    time.sleep(1)
    q.put((nick, nick, ["this should be a list", "test new privmsg"]))
