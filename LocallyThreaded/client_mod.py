import os, sys, socket, hashlib, pickle

hashedword = "4f9c4e19748be021372db6d5e10cfd02"

def main():
   target = '127.0.0.1'
   port = 5555

   chars = "abcdefghijklmnopqrstuvwxyz"
   charl = len(chars)

   while True:
      s = socket.socket()
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.connect((target,port))
      start = s.recv(1024)

      for i in xrange(charl):
         for j in xrange(charl):
            for k in xrange(charl):
               for l in xrange(charl):
                  word = start + chars[i] + chars[j] + chars[k] + chars[l]
                  print "Trying ", word
                  temp = hashlib.md5(word)
                  if temp == hashedword:
                     print word
                     sock = socket.socket()
                     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                     sock.connect((target,5556))
                     sock.send(word)
                     sock.close()
      s.close()

if __name__ == '__main__':
   main()
