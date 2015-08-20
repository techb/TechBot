# TechBot

This is an ircbot I will be working on. It support loading modules/plugins. 

It is written in Python 3.4.3 and is being tested on Arch Linux.

There is no official documentation on it yet, but code comments and doc-strings should tell you anything
you need to know.

SSL has been fixed, using Queues and Selector now. Examples have been updated in the adons.

No more issue with zombie processes. I have added a snippit to remove or '.join()' finished
multiprocesses that had been started as 'addons'.

Fixed spelling, adon has been chaged to addons as per everyone pointing it out lol.

---NOTICE---

Instead of code, you can fix spelling errors and such in the comments and all. Make a pull request
for what you fixed.

-----------


Logging has been added, you can log all, or filter phrases or words. This is done in the irc.config file
usign CSV. Look at the config file for an example.

--TO DO--

Start adding channel op things such as flood control and user logs (diff with host mask and last seen kinda things).

Timed things, such as random or certian points, post an update for something.

Random (current) links to hacking and securrity related stuff. Maybe a .hot command to grab links from security blogs.

EZ related things, like recent posts or stats or something.

User input?
