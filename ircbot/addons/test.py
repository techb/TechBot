import time

def main(nick, comargs, chan, send):
    '''nick is who sent the command, type string
    comargvs is anything after the command, such as a website or other supporting args, type string
    chan is either the channel to send to, or our own nick in which case is a private message
    send is now a queue. So we need to 'put' things into it.'''

    # example on sending a simple string to the default channel the bot is on
    print(nick)
    print(chan)
    print(comargs)
    time.sleep(1)
    send.put(("Success!", chan))

    # You can send just a string, it will go to the default channle you set in irc.config
    send.put("Success! No chan info provided, going to default channel")
