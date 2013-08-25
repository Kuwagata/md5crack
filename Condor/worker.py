#!/usr/bin/env python
import socket, pickle, commands, threading
import StringIO, sys

from subprocess import *

WORKER_HOST = socket.gethostbyname_ex(socket.gethostname())[2][0]
WORKER_PORT = 4000
SERVER_HOST = 'gecko3.cs.clemson.edu'
SERVER_PORT = 3580

def runcmd(cmdin):
   p = supbrocess.Popen(cmdin, stdout=subprocess.PIPE, shell=True)
   results = ""
   while True:
      line = p.stdout.readline()
      if not line: break
      results += line
   return results

class serverConn(threading.Thread):
   def __init__(self,sHost,sPort):
      threading.Thread.__init__(self)
      
      self.sHost = sHost
      self.sPort = sPort

      self.sock = socket.socket()
      self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
   def run(self):
      try:
         # Connect to server
         try:
            self.sock.connect((self.sHost,self.sPort))
         except:
            print "Cannot connect to central server"
            sys.exit()
         
         # Build and package classad, submit to server
         classad = {'node':'worker','os':'linux','ip':WORKER_HOST,'port':WORKER_PORT}
         pclassad = pickle.dumps(classad)
         self.sock.send(pclassad)
         
         # Wait for handshake
         response = self.sock.recv(1024)
         if response == 'error':
            print "Invalid worker node classad"
         elif response == 'success':
            print "Submitted worker node to central server"
         else:
            print "Invalid response from central server"

      except KeyboardInterrupt:
         print "Keyboard interrupt in server connection"
         self.sock.close()
         sys.exit()

      except:
         print "Error in central manager connection"
         print self.sHost
         print self.sPort

      self.sock.close()


class clientConn(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      self.sock = socket.socket()
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   def run(self):
      self.sock.bind(('',WORKER_PORT))
      self.sock.listen(1)
      try:
         # Accept connections
         while True:
            conn, addr = self.sock.accept()
            # For each connection run some # of commands
            while True:
               command = conn.recv(1024)
               print command
               if command == 'quit':
                  break
               elif command[:7] == 'python:':
                  datafile = command[7:]
                  output = StringIO.StringIO()
                  sys.stdout = output
                  exec datafile
                  sys.stdout = sys.__stdout__
                  results = output.getvalue()
                  output.close()
                  data = pickle.dumps(results)
                  conn.send(data)
               else:
                  output = ""
                  p = Popen(command, stdout=PIPE, shell=True)
                  while True:
                     line = p.stdout.readline()
                     if not line: break
                     output += line
                  data = pickle.dumps(output)
                  conn.send(data)
            conn.close()
      except KeyboardInterrupt:
         print "Keyboard interrupt in client connection"
         return
      except:
         print "Error in client thread"   

      self.sock.close()

def main():
   
   threadsList = []
   threadsList.append(serverConn(SERVER_HOST, SERVER_PORT))
   threadsList.append(clientConn())
   for thread in threadsList:
      thread.start()

   for thread in threadsList:
      thread.join()

if __name__ == '__main__':
   main()
