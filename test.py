import sentence
import nltk
import fileRead as fR

sentence_1 = "My name is Vishnu. I am a student at UCF."
sentnece_token = nltk.data.load('tokenizers/punkt/english.pickle')
lines = sentnece_token.tokenize(sentence_1)

for line in lines:
	print line

fR.readFile("file1")