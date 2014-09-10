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
 
stopset = list(stopwords.words('english'))
stopset.append("html")
stopset.append("htm")
exclude = list(string.punctuation)
exclude.append("''")
exclude.append("``")
exclude.append("'s")
 
stemmer = nltk.stem.SnowballStemmer("english")

trial = {}

def preprocess(repo, num_dir, num_file, chunk_size):
	j = 0
	for i in xrange(num_dir):
		pos = 0
		if i == 3 :
			continue
 
		while True:
			for k in xrange(chunk_size):
 
				try :
					f = open(repo + "/" + str(i) + "/" + str(j + k))
					print j + k
				except IOError :
					continue;
				try:
					html = f.read()
				except UnicodeDecodeError :
					f.close()
					continue;
				f.close()
				raw = nltk.clean_html(html)
 
				raw = raw.lower()
				word_tokenizer = nltk.RegexpTokenizer('\w+')
				tokens = word_tokenizer.tokenize(raw)
				temp = {}
				
				for w in tokens:
					if not w in exclude:
						try :
							w = stemmer.stem(w)
							w = w.encode('ascii')
						except :
							continue;
						
						if w not in temp:
							temp[w] = 1
						else :
							temp[w] += 1
				
				for w in temp:
					if w in trial:
						trial[w][0] += 1
						trial[w][1] += temp[w]
					else:
						trial[w] = [1, temp[w]]
				temp = {}

			j += chunk_size
			if (j == (i + 1) * num_file):
				break
 
preprocess("testdata", 1, 6, 2)

pickle.dump(trial, open('pickle/trial.dat', 'wb'))

print(datetime.now()-startTime)
