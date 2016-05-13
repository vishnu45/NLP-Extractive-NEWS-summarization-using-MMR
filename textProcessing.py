import nltk
import os
import string
import re
import sentence

def readFile(fileName):

	#read the given file to extract the sentences
	f = open(fileName,'r')
	text = f.read()	

	# extract content in TEXT tag and remove tags
	text = re.search(r"<TEXT>.*</TEXT>", text, re.DOTALL)	
	text = re.sub("<TEXT>\n", "", text.group(0))
	text = re.sub("\n</TEXT>", "", text)

	# #replace all types of quotations by normal quotes, etc
	text = re.sub("\n", " ", text)
	text = re.sub(" +", " ", text)
	text = re.sub("\'\'", "\"", text)
	text = re.sub("``", "\"", text)

	# segment data into a list of sentences
	sentence_token = nltk.data.load('tokenizers/punkt/english.pickle')
	lines = sentence_token.tokenize(text.strip())

	# setting stemmer
	porter = nltk.PorterStemmer()
	sentences = []

	# process each of the sentences, model each as a sentence object
	for line in lines:

	 	# keep the original words before the stemming process
		original_words = line

	 	# word tokenization
		line = line.strip().lower()

		sentence_tok = nltk.word_tokenize(line)

	 	# stemming words
	 	sentence_stemmed = [porter.stem(word) for word in sentence_tok]

	 	# remove punctuations
	 	sentence_stemmed = filter(lambda x: x!='.' and x!='?' and x!='!'
	 		and x!=',' and x!="'s", sentence_stemmed)

	 	# create the sentence object and add to the list of sentences
	 	sentences.append(sentence.sentence(sentence_stemmed, original_words))

	return sentences