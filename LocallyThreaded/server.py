import os, sys, socket, threading, math, time

# Thread to generate first 4 letters and serve them out
class wordgen(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      self.s = socket.socket()
      self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
      self.s.bind(('',5555))

   def run(self):
      # Characters to select from
      chars = "abcdefghijklmnopqrstuvwxyz"
      charl = len(chars)
      
      # Listen for workers
      self.s.listen(1)

      # Send out combinations of 4-letter words to start from
      for i in xrange(charl):
         for j in xrange(charl):
            for k in xrange(charl):
               for l in xrange(charl):
                  start = chars[i] + chars[j] + chars[k] + chars[l]
                  conn, addr = self.s.accept()
                  conn.send(start)

def main():
   t_start = time.time()
   # Create word generator and start it
   generator = wordgen()
   generator.start()

   # Wait for one of the workers to send a result back
   s = socket.socket()
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
   s.bind(('', 5556))
   s.listen(1)
   print "Waiting for response from client"
   conn, addr = s.accept()
   word = conn.recv(1024)
   t_end = time.time()
   print "Result: ", word
   print "Time: ", t_end - t_start, "s"
   os.exit(1)

if __name__ == '__main__':
   main()
