-------------------------------------------------------------------------------------------------------------------------------
	Readme: Generic Summarization
-------------------------------------------------------------------------------------------------------------------------------
  Project files and folders:
-------------------------------------------------------------------------------------------------------------------------------
project_root	: root folder of project containing all required files and folders
Documents	: news articles relating to 50 topics
Human_Summaries	: Human summaries used to evaluate the quality of system generated
		  summaries produced by LexRank and MMR approach
Lexrank_results	: folder which holds the system generated summaries of LexRank
MMR_results	: folder which holds the system generated summaries of MMR

sentence.py	: sentence class for modelling sentences in the document cluster
mmr_summarizer.py	: MMR implementation
LexRank.py	: LexRank implementation
test_pyrouge.py	: for generating the ROUGE scores for the system summaries
jaccardScore.py	: for generating jaccard coefficient at word and sentence level
-------------------------------------------------------------------------------------------------------------------------------
  System/software requirements:
-------------------------------------------------------------------------------------------------------------------------------
- python version 2.7
- pyRouge version 0.1.0
- ROUGE toolkit 1.5.5
-------------------------------------------------------------------------------------------------------------------------------
  How to run:
-------------------------------------------------------------------------------------------------------------------------------
- For generating the MMR system summaries run the mmr_summarizer.py. The results will be 
generated in the MMR_results folder.

- For generating the LexRank system summaries run the LexRank.py. The results will be generated 
in the Lexrank_results folder.

- For generating the ROUGE scores run the test_pyrouge.py. Results will be displayed on the terminal

- For generating the Jaccard coefficient scores run the jaccardScore.py. Both word and sentence 
level scores will be displayed on the screen
-------------------------------------------------------------------------------------------------------------------------------