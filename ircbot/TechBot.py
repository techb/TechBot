import irc
import os
import importlib

class TechBot(irc.Irc):
    def __init__(self):
        '''init this class, and also irc class.'''
        irc.Irc.__init__(self)
        self.adon_folder = "adons"
        self.adons = {}
        self.loadAllAdons()

    def test(self, x):
        '''debug to make sure adons where loaded, hasn't faild in a while now, juts respect file path'''
        self.adons[x].main()
        self.showDefaults()

    def loadAllAdons(self):
        '''adons are in /adons, ignore the cache (python3 lol), loads the dict with
        key = command/module name and value = module handle to exicute it's main()'''
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
            
    def handleCommand(self, data):
        '''As of right now on public publish, threads are not implemented
        so if a module fails, so will core. modules/adons can crash core atm.
        BUT will be fixed in the next week or so. Just give me a little time.'''
        if type(data) is tuple:
            who = data[0]
            command = data[1]
            chan = data[2]
            #check if it's a command, then send to approperate command module
            if command[0] == "!":
                com = command.split()[0][1:].strip() #get command name minus the !
                comargv = " ".join(command.split()[1:]).strip() #get argument/s
                if com in self.adons.keys():
                    modreturn = self.adons[com].main(who, comargv, chan)
                    self.sendIrc(modreturn)
            
    def main(self):
        '''handleData() will be gone soon, so take it as it is for the moment. this main() will be
        to handle command input, or sub-forward to irc class to handle internals. This method will change.
        Modules writers don't need to worry about it though. This is a core dev thing.'''
        while True:
            fulldata = self.recvData()
            print(fulldata)
            if fulldata:
                data = self.handleData(fulldata)
                self.handleCommand(data)
                
# And so we begin.
if __name__ == "__main__":
    bot = TechBot()
    bot.main()
