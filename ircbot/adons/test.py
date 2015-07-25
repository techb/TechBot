def main(nick, comargvs, chan):
    print(nick)
    print(comargvs)
    print(chan)
    print("module has ran")
    
    #This is what your module returns as it's out put. It REQUIRES it to be
    #    a list, message returns a list, not a tupe, not a string but a LIST.
    message = ["My return here"]
    
    #MUST return a tuple in this order.
    #nick is who sent it
    #chan is either the channel it was sent on OR our own nick, if our own
    #    nick is equal to chan, it is a private message, irc.py will handle it 
    #    anyway. But return it anyway so irc.py can handle it.
    #message is what ever you want to send, it is the return of what your module does.
    return (nick, chan, message)
