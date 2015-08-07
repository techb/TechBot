import time

def main(nick, comargs, chan, send):
    '''nick is who sent the command type of string
    comargvs is anything after the command, such as a website or other supporting args  of type string
    chan is either the channel to send to, or our own nick in which case is a private message
    send is now a queue. So we need to 'put' things into it.
    
    irc.py -> sendIrc() holds le answers for now, just give me time.'''
    
    # example on sending a simple string to the default channel the bot is on
    print("[*] Testing simple default")
    time.sleep(1)
    send.put("Success!")
