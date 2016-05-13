import textProcessing as tp
import nltk
import os
import string
import math
	
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
		sentences = tp.readFile(curr_folder + "/" + file)

		# doc_cluster = doc_cluster + sentences