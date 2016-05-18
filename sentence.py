

class sentence(object):

	#-------------------------------------------------------------------
	# Description	: Constructor to initialize the sentence object
	# Parameters	: stemmedWords, words of the sentence after stemming
	#				  originalWords, actual words before stemming
	# Return 		: None
	#-------------------------------------------------------------------
	def __init__(self, stemmedWords, originalWords):
		self.stemmedWords = stemmedWords
		self.originalWords = originalWords
		self.wordFreq = self.wordFrequencies();

	#-------------------------------------------------------------------
	# Description	: 
	# Parameters	: 
	#				  
	# Return 		: 
	#-------------------------------------------------------------------
	def getStemmedWords(self):
		return self.stemmedWords

	#-------------------------------------------------------------------
	# Description	: 
	# Parameters	: 
	#				  
	# Return 		: 
	#-------------------------------------------------------------------
	def getOriginalWords(self):
		return self.originalWords

	#-------------------------------------------------------------------
	# Description	: 
	# Parameters	: 
	#				  
	# Return 		: 
	#-------------------------------------------------------------------
	def getWordFreq(self):
		return self.wordFreq

	#-------------------------------------------------------------------
	# Description	: Function to create a dictonary of word frequencies
	#				  for the sentence object
	# Parameters	: None
	# Return 		: dictionary of word frequencies
	#-------------------------------------------------------------------
	def wordFrequencies(self):
		wordFreq = {}
		for word in self.stemmedWords:
			if(word not in wordFreq.keys()):
				wordFreq[word] = 1
			else:
				wordFreq[word] += 1
		return wordFreq