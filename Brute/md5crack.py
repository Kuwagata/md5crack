import os, sys, hashlib, time

def crack(hashed):
   # Characters to select from
   chars = "abcdefghijklmnopqrstuvwxyz"
   charl = len(chars)

   # Try each combination
   for i in xrange(charl):
      for j in xrange(charl):
         for k in xrange(charl):
            for l in xrange(charl):
               # Calculate the hash of each combination and return if it matches
               word = chars[i] + chars[j] + chars[k] + chars[l]
               temp = hashlib.md5(word)
               if temp.hexdigest() == hashed:
                   return word

def main():
   tocrack = hashlib.md5(sys.argv[1]).hexdigest()
   print "Attempting to crack '", sys.argv[1], "'"
   print "Hash: ", tocrack
   time_start = time.time()
   print crack(tocrack)
   time_stop = time.time()
   print time_stop - time_start

if __name__ == '__main__':
   main()
