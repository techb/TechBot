'''Every thing is working now. Zombies have also been taken care of. logging
implemented in irc.py'''

import irc
import os
import importlib
import multiprocessing
import time
import ssl
import selectors


class TechBot(irc.Irc):
    def __init__(self):
        '''init this class, and also irc class.'''
        irc.Irc.__init__(self)
        self.addon_folder = "addons"
        self.addons = {}
        self.loadAlladdons()
        self.process_list = []
        self.prepender = "."
        print("[+] init finished")


    def loadAlladdons(self):
        '''addons are in /addons, ignore the cache (python3 lol), loads the dict with
        key = command/module name and value = module handle to exicute it's main()
        ToDo: os.glob would probably be better here.'''
        addon_names = os.listdir(self.addon_folder)
        for addon in addon_names:
            # ignore the cache
            if addon == "__pycache__":
                continue
            addon = addon.split('.')[0] # take the .py off
            # dynamically load modules from absolute path
            mod = importlib.import_module('.'.join((self.addon_folder, addon)))
            self.addons[addon] = mod # dict key=name value=object handle
        print("[+] Addons loaded.")

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

    def checkCommand(self, data, q):
        '''This checks whether its a command or not and sees if we have a module tohandle it.
        If we do, start a new process, the new process will send results to the queue'''
        if type(data) is tuple:
            who = data[0]
            command = data[1]
            chan = data[2]
            # check if it's a command, then send to approperate command module
            if command[0] == self.prepender:
                com = command.split()[0][1:].strip() # get command name minus the prepender
                comargv = " ".join(command.split()[1:]).strip() # get argument/s
                if com in self.addons.keys():
                    com_process = multiprocessing.Process(target=self.addons[com].main, args=(who, comargv, chan, q))
                    com_process.start()
                    self.process_list.append(com_process)
                    print("[+] Found and ran addon %s" % com)
                else:
                    print("[-] Not Found")

    def main(self):
        '''This method, since it's main, will be under construction till I'm happy with it.
        Went back to using queues. Also using select. SSL issues have been solved. Anything
        in a queue is to be sent to the irc chan.'''
        # SimpleQueue because .empty() is safer than regular Queue
        q = multiprocessing.SimpleQueue()
        # Python3 recommends using selector instead of select unless you need finer control
        sel = selectors.DefaultSelector()
        sel.register(self.sock, selectors.EVENT_READ, self.recvData)
        while True:
            if not q.empty():
                d = q.get()
                if type(d) == tuple:
                    self.sendIrc(d[0], to=d[1])
                else:
                    self.sendIrc(d)

            event = sel.select(.1) # timeout .1, else it'll block making the queue useless.
            if event:
                for key, mask in event:
                    callback = key.data
                    fulldata = callback(key.fileobj)
                if fulldata:
                    data = self.handleData(fulldata)
                    check = self.checkCommand(data, q)

            # loop through a copy of the list of sub processes and join any zombies, then remove from list
            for subproc in self.process_list[:]:
                if not subproc.is_alive():
                    subproc.join()
                    self.process_list.remove(subproc)

# And so we begin.
if __name__ == "__main__":
    bot = TechBot()
    bot.main()
