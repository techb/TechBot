import time

def main(nick, comargvs, chan, send):
    '''nick is who sent the command type of string
    comargvs is anything after the command, such as a website or other supporting args  of type #todo
    chan is either the channel to send to, or our own nick in which case is a private message
    
    send is the method from the base class irc.sendIrc
    I will add more examples here soon to show how we can use it.
    For now, I just send a string for testing'''
    time.sleep(5)
    send("Success!")
    
