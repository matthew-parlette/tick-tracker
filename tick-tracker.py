#!/usr/bin/python
import os

shutdown = False

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
  def __init__(self):
    self.name = "Project"
    self.ticks = 0

class Menu(object):
  def __init__(self, items = dict()):
    self.items = items
    self.getch = _GetchUnix()
    self.error = None
  
  def display(self):
    os.system('clear')
    print "Error: %s" % self.error if self.error else ""
    print "Projects"
    print "--------\n"
    if self.items:
      for item in self.items:
        print item
    else:
      print "Nothing to see here"
    print ""
    print("cmd > "), #no newline
    self.command(self.getch())
  
  def command(self,command):
    command = command
    if command in ('q','Q'):
      global shutdown
      shutdown = True
    if command in ('a','A'):
      pass 

def loop(menu):
  while not shutdown:
    menu.display()

if __name__ == "__main__":
  menu = Menu()
  loop(menu)
