import socket
import ssl
import configparser
import os
import atexit

class Irc:
    def __init__(self, cfg_file=None):
        ''''Setup default info for bot. If cfg_file is not provided, deafult is used.'''
        self.cfg = configparser.ConfigParser(allow_no_value=True)

        # need to implement better file path handling
        if cfg_file:
            self.cfg.read(cfg_file)
        else:
            self.cfg.read("irc.config")

        # setup server info, convert types as needed
        self.server = self.cfg.get("ircserver", "server")
        self.use_ssl = self.cfg.getboolean("ircserver", "ssl")
        if self.use_ssl:
            self.port = self.cfg.getint("ircserver", "sslport")
        else:
            self.port = self.cfg.getint("ircserver", "dport")

        # prepend '#' to channels
        # multi-channel not supported yet, should be handled in ircInit()
        self.channel = "#"+self.cfg.get("channels", "dchannel")
        self.poschan = self.cfg.options("channels")[1:] # [0] is default, not needed here

        print(self.poschan)
        self.nick = self.cfg.get("nameinfo", "dnick")
        self.realname = self.cfg.get("nameinfo", "realname")
        self.nickserv_pass = self.cfg.get("nameinfo", "nickserv_pass")

        # setup logging
        self.log_all = self.cfg.getboolean("logging", "log_all")
        self.log_filter = self.cfg.getboolean("logging", "log_filter")
        if self.log_filter:
            self.log_filters = self.cfg.get("logging", "filters").split(',')
            self.log_filters = [x.strip() for x in self.log_filters]
        print("[+] Reading config file finished.")

        print("[+] Creating socket.")
        try:
            self.sock = self.getSocket()
        except:
            print("[!] Failed creating socket.")

        atexit.register(self.handleExit)
        self.ircInit()

    def getSocket(self):
        '''Creates and returns the socket handle. This object instance should remain in this class.
        anything pertaining to irc connections, this class should explicitaly handle it.
        set socket timeout to 0.0 for non-blocking.'''
        if self.use_ssl:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sslsock = ssl.wrap_socket(s)
            sslsock.connect((self.server, self.port))
            print("[+] Connected to %s on port %d" % (self.server, self.port))
            return sslsock
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server, self.port))
            print("[+] Connected to %s on port %d" % (self.server, self.port))
            #sock.setblocking(False)
            return sock

    def sendIrc(self, data, chan=None):
        '''if it's just a string, assume it's a message we send to default channel
        check if private message, and send to who it needs to be sent.
        if chan is our nick, then it's private message'''
        if chan == None:
            chan = self.channel
        if type(data) == str:
            self.sendData("PRIVMSG %s :%s\r\n" % (chan, data))
            return

        # There is a better way to do this, will work on it soon.
        print(data)
        nick = data[0]
        chan = data[1]
        message = data[2]
        if type(message) != list:
            print("[-] Module didn't return message as list, ignoring")

        elif chan == self.nick:
            print("[+] Sent priv message to %s" % nick)
            for line in message:
                self.sendData("PRIVMSG %s :%s\r\n" % (nick, line))
        else:
            print("[+] Sent message to %s" % chan)
            for line in message:
                self.sendData("PRIVMSG %s :%s\r\n" % (chan, line))

    def sendData(self, data):
        '''sends the data, we have to encode because Python3 sting leterals are unicode'''
        self.sock.send(data.encode("utf-8"))

    def recvData(self, sock):
        '''decode received data because unicode, process basic irc stuff here
        like ping/pong, ect... Added logging.'''
        data = sock.recv(1024).decode("utf-8")
        if data[:4] == "PING":
            self.sendData("PONG :%s\r\n" % data.split(":")[1])

        # write log data to file
        if self.log_all:
            print(data)
            with open("log.txt", 'a') as logfile:
                logfile.write(data)

        elif not self.log_all and self.log_filter:
            for f in self.log_filters:
                if f in data.strip():
                    print(data)
                    with open("log.txt", 'a') as logfile:
                        logfile.write(data)

        return data

    def ircInit(self):
        '''initiate irc connection, send our user info wait for our info to go through.
        when we see 004 RPL_MYINFO, then we join the default channel. As per rfc2812 irc
        servers send 001 through 004 upon succesful connection.'''
        self.sendData("NICK %s\r\n" % self.nick)
        self.sendData("USER %s 0 * :%s\r\n" % (self.nick, self.realname))
        while True:
            data = self.recvData(self.sock)
            if data:
                if "004 %s" % self.nick in data:
                    self.sendData("JOIN %s\r\n" % self.channel)
                    if self.poschan:
                        for c in self.poschan:
                            print(c)
                            self.sendData("JOIN #%s\r\n" % c)
                    break

    def handleExit(self):
        '''If this program exits, run this method, used to clean up open handles.'''
        print("-"*20)
        print("[!] Something happened, closing socket and exiting.")
        print("-"*20)
        self.sock.close()
