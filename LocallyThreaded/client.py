import os, sys, socket, hashlib

hashedword = "4f9c4e19748be021372db6d5e10cfd02"

def main():
   # Target server to retrieve orders from
   target = 'dragon4.cs.clemson.edu'
   port = 5555

   # Characters to select from
   chars = "abcdefghijklmnopqrstuvwxyz"
   charl = len(chars)
   
   # Keep grabbing starting combinations from the master server
   while True:
      # Create a new socket
      s = socket.socket()
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.connect((target,port))
      
      # Retrieve first 4 letters from server
      try:
         start = s.recv(1024)
      except socket.timeout:
         os._exit(1)

      # Try combinations of last 4 letters with first 4
      for i in xrange(charl):
         for j in xrange(charl):
            for k in xrange(charl):
               for l in xrange(charl):
                  # Hash the word and compare it - send it back to server if it matches
                  word = start + chars[i] + chars[j] + chars[k] + chars[l]
                  temp = hashlib.md5(word)
                  if temp.hexdigest() == hashedword:
                     print word
                     sock = socket.socket()
                     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                     sock.connect((target,5556))
                     sock.send(word)
                     sock.close()
                     os._exit(1)
      s.close()

if __name__ == '__main__':
   main()
