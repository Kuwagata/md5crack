#!/usr/bin/env python

import httplib, socket, urllib2, sys, os, pickle, threading

# classad keys
WORKER = 'worker'
SUBMIT = 'submit'
NODE = 'node'
IP = 'ip'
OS = 'os'
PORT = 'port'
ERROR = 'error'
SUCCESS = 'success'

class newconn(threading.Thread):
   def __init__(self,conn,workerlist):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.conn = conn
      self.workers = workerlist
   def run(self):
      msg = self.conn.recv(1024)
      classad = pickle.loads(msg)

      if classad[NODE] == WORKER:
         if (PORT not in classad) or (IP not in classad):
            print "Could not add worker (IP or port not specified)"
            self.conn.send(ERROR)
         else:
            self.workers[classad[IP]] = classad
            print "Added worker IP", classad[IP]
            self.conn.send(SUCCESS)

      elif classad[NODE] == SUBMIT:
         # find a matching worker
         for ip in self.workers.keys():
            worker = self.workers[ip]
            for w in worker.keys():
            # w = worker node classad key
               match = True
               for s in classad.keys():
               # s = submit node classad key
                  if s not in {}.fromkeys((IP, PORT, NODE)):
                  # make sure we're not matching the IP, port, or node type
                     if s not in worker.keys():
                     # submit node has a requirement not IN the worker dict
                        match = False
                        break
                     elif classad[s] != worker[s]:
                     # submit node has a requirement not MET by the worker dict
                        match = False
                        break
               if match:
                  self.conn.send(pickle.dumps(worker))
                  print "Delivered worker", worker[IP],":",worker[PORT]
                  break
         if not match:
            print "Could not find a matching worker"
            self.conn.send(ERROR)

         self.conn.close()

def main():
   workerlist = {}
   HOST=''
   PORT=3580
   s=socket.socket()
   s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
   s.bind((HOST, PORT))
   s.listen(1)
   while True:
      conn, addr = s.accept()
      newconn(conn,workerlist).start()

if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      print "Interrupt by user"
      sys.exit()
   except:
      print "Unexpected error in server"
      sys.exit()
