import textProcessing as tp
import nltk
import os
import string
import math

#---------------------------------------------------------------------------------
# Description	: Function to find the term frequencies of the words in the
#				  sentences present in the provided document cluster
# Parameters	: sentences, sentences of the document cluster
# Return 		: dictonary of word, term frequency score
#---------------------------------------------------------------------------------
def TFw(sentences):
	# initialize TFS dictionary (word, value)
	tfs = {}

	# for every sentence in the document cluster
	for sent in sentences:
		# retrieve word frequency for each sentence object
		wordFreq = sent.getWordFreq()

		# build the word dictionary
		for word in wordFreq.keys():

			# if word already present in the dictonary
			if tfs.get(word, 0) != 0:
				tfs[word] = tfs[word] + wordFreq[word]

			# else if word is being added for the first time
			else:
				tfs[word] = wordFreq[word]			
	return tfs
	
# -------------------------------------------------------------
#	MAIN FUNCTION
# -------------------------------------------------------------
if __name__=='__main__':

	# set the main Document folder path where the subfolders are present
	main_folder_path = os.getcwd() + "/Documents"

	# read in all the subfolder names present in the main folder
	for folder in os.listdir(main_folder_path):

		print "Running MMR Summarizer for files in folder: ", folder
		# for each folder run the MMR summarizer and generate the final summary
		curr_folder = main_folder_path + "/" + folder		

		# find all files in the sub folder selected
		files = os.listdir(curr_folder)

		# list of all sentences from each file in the document cluster
		doc_cluster = []

		for file in files:
			print file
			doc_cluster = doc_cluster + tp.readFile(curr_folder + "/" + file)

		TFSs = TFw(doc_cluster)