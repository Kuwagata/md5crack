#!/usr/bin/env python
import socket, os, sys, pickle, threading, Queue, time, socklib

class getInput(threading.Thread):
   def __init__(self,cmdqueue):
      threading.Thread.__init__(self)
      self.cmdqueue = cmdqueue
   def run(self):
      try:
         while True:
            cmd = raw_input()
            if cmd == 'quit':
               break
            if cmd == 'python':
               print "Enter filename: "
               fname = raw_input()
               f = open(fname, 'r')
               cmd = cmd + ':' + f.read()
               f.close()
            self.cmdqueue.put(cmd)
      except EOFError:
         print "EOF error in input thread"
      
def main():
   # Specify server host/port and connect
   HOST, PORT = 'gecko3.cs.clemson.edu', 3580

   stillLooking = True
   while stillLooking:

      sock = socket.socket()
      try:
         sock.connect((HOST,PORT))
      except: 
         print "Cannot connect to central server"
         sys.exit()

      # Create classad, package data, submit to server
      classad = {'node':'submit', 'os':'linux'}
      pclassad = pickle.dumps(classad)
      sock.send(pclassad)

      # Wait for server to find a machine
      data = sock.recv(1024)
      sock.close()
      if data == "error":
         # try again in one second
         time.sleep(1)
      else:
         stillLooking = False

   
   # Unload machine info
   workerInfo = pickle.loads(data)
   print workerInfo

   HOST = workerInfo['ip']
   PORT = workerInfo['port']

   # Connect to worker
   cmdqueue = Queue.Queue()
   getInput(cmdqueue).start()
   csock = socket.socket()
   try:
      csock.connect((HOST,PORT))
   except:
      print "cannot connect to worker"
      sys.exit()
   
   print "Connected to worker"

   try:
      while True:
         # Keep retrieving commands
         command = cmdqueue.get()
         print "sending: ", command
         csock.send(command)
         if command == 'quit':
            break
         cmdres = csock.recv(4096)
         output = pickle.loads(cmdres)
         print output
   except:
      print "Problem retrieving commands from queue and sending"
   csock.close()

if __name__ == '__main__':
   main()
#   try:
#      main()
#   except:
#      print "Error in client"
