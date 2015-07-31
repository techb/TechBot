'''This needs to be restructured. Modules should have at least access to irc.sendIrc()
It's abstract enough to where they only need little knowledge of it. Plus it would clean
this class up a lot. I need a day with no distractions and just do it, we'll see....'''

import irc
import os
import importlib
import multiprocessing
import queue
import time


class TechBot(irc.Irc):
    def __init__(self):
        '''init this class, and also irc class.'''
        irc.Irc.__init__(self)
        self.adon_folder = "adons"
        self.adons = {}
        self.loadAllAdons()


    def loadAllAdons(self):
        '''adons are in /adons, ignore the cache (python3 lol), loads the dict with
        key = command/module name and value = module handle to exicute it's main()
        ToDo: os.glob would probably be better here.'''
        adon_names = os.listdir(self.adon_folder)
        for adon in adon_names:
            # ignore the cache
            if adon == "__pycache__":
                continue
            adon = adon.split('.')[0] # take the .py off
            # dynamically load modules from absolute path
            mod = importlib.import_module('.'.join((self.adon_folder, adon)))
            self.adons[adon] = mod # dict key=name value=object handle
            
    def handleData(self, data):
        '''Handles on PRIVMSG atm, anything else [I.E.] irc stuff should be handled in the irc class.
        irc.recvData SHOULD handle disconnects and stuff. irc.recvData SHOULD only return PRIVMSGs but I
        am tring to push public, this will all eventually change. Module writers will have nothign to worry about thoug.'''
        if "PRIVMSG" in data:
            who = data.split(":")[1].split("!")[0].strip()
            msg = data.split(":")[-1].strip()
            where = data.split(":")[1].split("PRIVMSG")[1].strip()
            return (who, msg, where)
        else:
            return data
            
    def checkCommand(self, data):
        '''This checks whether its a command or not and sees if we have a module to
        handle it.'''
        if type(data) is tuple:
            who = data[0]
            command = data[1]
            chan = data[2]
            # check if it's a command, then send to approperate command module
            if command[0] == "!":
                com = command.split()[0][1:].strip() # get command name minus the !
                comargv = " ".join(command.split()[1:]).strip() # get argument/s
                if com in self.adons.keys():
                    return (who, comargv, chan, self.adons[com])
                else:
                    return "NOT FOUND"

    def main(self):
        '''This method, since it's main, will be under construction till I'm happy with it.
        For now, we don't use queues anymore and just pass the send function as an argument to
        the subprocess. Using SSL is giving some weired errors, so I'm not using it till I can
        check out pyopenssl or something. I'll file an issue or something soon.'''
        while True:
            fulldata = self.recvData()
            if fulldata:
                print(fulldata)
                data = self.handleData(fulldata)
                check = self.checkCommand(data)
                if check:
                    if check == "NOT FOUND":
                        self.sendIrc("Command not found")
                        continue # nothing else to do, so go back to main loop
                    else:
                        print("Command found and ran")
                        print(check)
                        com_process = multiprocessing.Process(target=check[3].main, args=(check[0], check[1], check[2], self.sendIrc))
                        com_process.start()

# And so we begin.
if __name__ == "__main__":
    bot = TechBot()
    bot.main()
