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
 
terms = pickle.load(open("pickle/final.dat", 'rb'))
stopword = {}
for word in stopset:
	if word in terms:
		stopword[word] = terms.pop(word)

index_terms = []
for s in terms.keys():
	try:
		s = s.encode('ascii')
		index_terms.append(s)
	except:
		continue;
index_terms = sorted(index_terms)
 
#print index_terms
 
#for i in index_terms:
#	print i, terms[i]
 
starting_pos = 0

for i in index_terms:
	terms[i].append(starting_pos)	# next occurrence of i will b stored here. Variable
	starting_pos += (2 * terms[i][0] + terms[i][1]) * 8
	#collection freq no longer needed, so that position will store smthing else	
	terms[i][1] = terms[i][2];		#posting list for i starts here. Fixed
 
print "---------------------------------"
 
#for i in index_terms:
#	print i, terms[i]
 
print index_terms[-1]
g = open("index/postings", "rb+")
g.seek(terms[index_terms[-1]][2] - 1)
g.write("\0")
g.seek(0)
print os.stat("index/postings").st_size


def preprocess(repo, num_dir, num_file, chunk_size):
	j = 0
	temp = {}
	for i in xrange(num_dir):
		if i == 3 :continue
		while True:
			for k in xrange(chunk_size):
 				pos = 0
				try :
					f = open(repo + "/" + str(i) + "/" + str(j + k))
					print j + k
				except IOError : continue;
				try: html = f.read()
				except UnicodeDecodeError :
					f.close()
					continue;
				f.close()
				raw = nltk.clean_html(html)
 
				raw = raw.lower()
				word_tokenizer = nltk.RegexpTokenizer('\w+')
				tokens = word_tokenizer.tokenize(raw)
				#print tokens
				
 				for w in tokens:
					if not w in exclude:
						try : 
							w = stemmer.stem(w)
							w = w.encode('ascii')
						except :
							continue;
						
						if not w in stopset:
							pos += 1
							if w not in temp:
								temp[w] = [[j + k, 1, [pos]]]
							else :
								if (temp[w][-1][0] == j + k):
									temp[w][-1][1] += 1
									temp[w][-1][2].append(pos)
								else:
									temp[w].append([j + k, 1, [pos]])
 
			j += chunk_size
			if (j == (i + 1) * num_file):
				break
 
		index_terms = sorted(temp.keys())
		for t in index_terms:
			g.seek(terms[t][2] - g.tell(), 1)
			print temp[t]
			for l in temp[t]:
				g.write(struct.pack("<q", l[0]))
				#g.write(",")
				g.write(struct.pack("<q", l[1]))
				#g.write(",")
				for pos in l[2]:
					g.write(struct.pack("<q", pos))
					#g.write(",")
				
				terms[t][2] = g.tell()	
		temp = {}
 
preprocess("repo", 2, 10000, 5000)
g.close()
pickle.dump(terms, open('pickle/non_stopword.dat', 'wb'))
pickle.dump(stopword, open('pickle/stopword.dat', 'wb'))

print(datetime.now()-startTime)