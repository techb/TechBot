import socket
import ssl
import configparser
import os
import sys
import atexit
import traceback
import time

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
        self.admin = self.cfg.get("ircserver", "admin")
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
        except ConnectionRefusedError:
            print("[!] Peer refused connection, try again.")
            sys.exit()
        except:
            print("[!] Something went wrong, here's the traceback.")
            traceback.print_exc()
            sys.exit()

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
            return sock

    def sendIrc(self, data, to):
        '''Sends a string off to be sent to the irc. Data is said string
        to is where it goes.'''
        if type(data) == str:
            self.sendData("PRIVMSG %s :%s\r\n" % (to, data))
            print("PRIVMSG %s :%s\r\n" % (to, data))
        else:
            print("[!] Data not string, check your addon")

    def sendData(self, data):
        '''sends the data, we have to encode because Python3 sting leterals are unicode'''
        self.sock.send(data.encode("utf-8"))

    def recvData(self, sock):
        '''decode received data because unicode, process basic irc stuff here
        like ping/pong, ect... Added logging. Added rejoin after kcik.'''
        data = sock.recv(4096)
        if "PING" in data:
            self.sendData("PONG :%s\r\n" % data.split(":")[1])

        if "KICK" in data:
            kdata = data.split("KICK")[1].strip().split(":")[0]
            if self.nick in kdata and self.channel in kdata:
                print("was kicked")
                time.sleep(5)
                print("trying rejoin")
                self.sendData("JOIN %s\r\n" % self.channel)

        # write log data to file
        if self.log_all:
            print(data.encode("utf-8"))
            with open("log.txt", 'a') as logfile:
                logfile.write(data)

        elif not self.log_all and self.log_filter:
            for f in self.log_filters:
                if f in data.strip():
                    print(data.encode("utf-8"))
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
                            self.sendData("JOIN #%s\r\n" % c)
                            print("[+] Joining %s" % c)
                    break

    def handleExit(self):
        '''If this program exits, run this method, used to clean up open handles.'''
        print("-"*20)
        print("[!] Something happened, closing socket and exiting.")
        print("-"*20)
        self.sock.close()
