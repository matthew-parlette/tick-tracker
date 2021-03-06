#!/usr/bin/python
import os
import string
import cPickle as pickle

shutdown = False
tick_scale = 30 #minutes
session_filename = "last_session.p"

class _GetchUnix:
  def __init__(self):
    import tty, sys

  def __call__(self):
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Project(object):
  def __init__(self,name):
    self.name = name
    self.ticks = 0
  
  def __repr__(self):
    return "%s (%s)" % (self.name,str(self.ticks * tick_scale))
  
  def restart(self):
    """Reset the project to 0 ticks."""
    self.ticks = 0
  
  def tick(self, ticks = 1):
    self.ticks += ticks

class Menu(object):
  def __init__(self, items = dict()):
    # if items is empty, try to load from session_filename
    try:
      self.items = pickle.load( open( session_filename, "rb" ) )
      # clear all ticks from loaded items
      for option, item in self.items.iteritems(): item.restart()
    except:
      self.items = items
    
    self.commands = {'q':'Quit','a':'Add Project','d':'Delete Project'}
    self.getch = _GetchUnix()
    self.error = None

  def add_item(self, project, option = None):
    if option is None:
      # assign it a key
      order = list(string.printable)
      for k in order:
        if not self.items.has_key(k) and not self.commands.has_key(k) and option is None: # very inefficient
          option = k
        
    if self.items.has_key(option):
      self.error = "Option %s already exists!" % option
    else:
      self.items[option] = project
  
  def display(self):
    os.system('clear')
    print "Error: %s" % self.error if self.error else ""
    print "Tick Scale: %s minutes" % (tick_scale)
    print "----------------------\n"
    print "Projects"
    print "--------\n"
    if self.items:
      for key,value in sorted(self.items.iteritems()):
        print "%s. %s" % (key,value)
    else:
      print "Nothing to see here"
    
    print "\n--------"
    for key,value in sorted(self.commands.iteritems()):
        print "%s. %s" % (key,value)
    
    print ""
    print("cmd > "), #no newline
    self.command(self.getch())
  
  def command(self,command):
    command = command
    if command in ('q','Q'):
      global shutdown
      shutdown = True
      
      #save the current item list
      pickle.dump( self.items, open( session_filename, "wb" ) )
    if command in ('a','A'):
      name = raw_input("New Project > ")
      self.add_item(Project(name))
    if command in ('d','D'):
      print("Delete Project > "), #no newline
      option = str(self.getch())
      if self.items.has_key(option): del self.items[option]
    if self.items.has_key(command):
      print "command is %s" % command
      print "project found as %s" % self.items[command]
      self.items[command].tick()

def loop(menu):
  while not shutdown:
    menu.display()

if __name__ == "__main__":
  menu = Menu()
  loop(menu)
