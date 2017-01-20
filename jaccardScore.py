from __future__ import division
import os
import nltk
from sklearn.metrics import jaccard_similarity_score
import itertools


def jaccard_word_score(setOfWords_1, setOfWords_2):
	set1 = set(setOfWords_1)
	set2 = set(setOfWords_2)
	U = set(set1).union(set2)
	I = set(set1).intersection(set2)
	return len(I)/len(U)


if __name__=='__main__':

	# Initialize MMR and LexRank result folders
	mmr_folder = os.getcwd() + "/MMR_results"
	lexrank_folder = os.getcwd() + "/Lexrank_results"
	
	# Initialize jaccard coefficicent for word level and sentence level
	jaccard_w_values = []
	jaccard_s_values = []

	# Start reading each file	
	files = os.listdir(mmr_folder)
	for file in files:
		# read all words from mmr file
		with open(mmr_folder + "/" + file) as f:
			mmr_words = f.read().split()
		# read all words from lexrank file
		with open(lexrank_folder + "/" + file[:-3] + "LexRank") as f:
			lex_words = f.read().split()	
		# calculate jaccard coefficeint for mmr vs lexrank file
		jaccard_w_values.append(jaccard_word_score(mmr_words, lex_words))		

	# find average jaccard coefficient score at word level
	avg_jaccard_w = sum(jaccard_w_values) / len(jaccard_w_values)
	print "Word level avaerage Jaccard score: ", round(avg_jaccard_w,4)

	# for sentence split 
	sentence_token = nltk.data.load('tokenizers/punkt/english.pickle')

	# Start reading each file	
	for file in files:
		# read sentences from mmr file
		with open(mmr_folder + "/" + file) as f:
			content = f.read()
		mmr_sentences = sentence_token.tokenize(content.strip())
		# read sentences from lexrank file
		with open(lexrank_folder + "/" + file[:-3] + "LexRank") as f:
			content = f.read()
		lex_sentences = sentence_token.tokenize(content.strip())

		jaccard_s_values.append(jaccard_word_score(mmr_sentences, lex_sentences))

	avg_jaccard_s = sum(jaccard_s_values) / len(jaccard_s_values)
	print "Sentence level avaerage Jaccard score: ", avg_jaccard_s