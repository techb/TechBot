import time

def main(nick, comargs, chan, send) :
    '''Test showing sending pm.'''
    print(nick)
    print(chan)
    print(comargs)
    time.sleep(1)
    send.put(("testing yo.", nick))
