# import fileRead
# import sentence
# import rougeScore
import nltk
import os
	
# set the main Document folder path where the subfolders are present
main_folder_path = os.getcwd() + "/Documents"

# read in all the subfolder names present in the main folder
for folder in os.listdir(main_folder_path):

	print "Running MMR Summarizer for files in folder: ", folder
	# for each folder run the MMR summarizer and generate the final summary
	curr_folder = main_folder_path + "/" + folder		

	# find all files in the sub folder selected
	files = os.listdir(curr_folder)

	