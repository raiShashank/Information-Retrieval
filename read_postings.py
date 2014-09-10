import pickle
import os
import nltk
from nltk.corpus import stopwords
import string
import pickle
from datetime import datetime
import codecs
import os
import struct

startTime = datetime.now()

non_stopword = pickle.load(open('pickle/non_stopword.dat', 'rb'))

#print non_stopword
print os.stat("index/postings").st_size
#index_terms = sorted(non_stopword.keys())
index_terms = []
for s in non_stopword.keys():
	try:
		s = s.encode('ascii')
		index_terms.append(s)
	except:
		continue;
index_terms = sorted(index_terms)

#for t in index_terms:
#	print t, non_stopword[t]

g = open("index/postings", "rb")
#only have to read the file here
flag = False
for t in index_terms:
	print t, "starts at", non_stopword[t][1]
	if (non_stopword[t][2] > non_stopword[t][1]): flag = True
	else: 
		print "Not appeared"
		continue
	g.seek(non_stopword[t][1])
	for i in xrange(non_stopword[t][0]):
		
		a = g.read(8)
		a = struct.unpack("<q", a)
		print '"', t, '" appears in doc ', a[0],
		
		a = g.read(8)
		a = struct.unpack("<q", a)
		print a[0], " times at pos :",
		tf = a[0]
		for j in xrange(tf):
			
			a = g.read(8)
			a = struct.unpack("<q", a)
			print a[0],

	print
	if flag:
		break
g.close()
print(datetime.now()-startTime)
