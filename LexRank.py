import os
import math
import numpy
import copy
import nltk
from bs4 import BeautifulSoup
import re

class LexRank(object):
    def __init__(self):
        self.text = Preprocessing()
        self.sim = DocumentSim()
    def score(self, sentences, idfs, CM, t):

        Degree = [0 for i in sentences]
        L = [0 for i in sentences]
        n = len(sentences)
        
        for i in range(n):
            for j in range(n):
                CM[i][j] = self.sim.sim(sentences[i], sentences[j], idfs)
                
                if CM[i][j] > t:
                    CM[i][j] = 1
                    Degree[i] += 1
                    
                else:
                    CM[i][j] = 0

        for i in range(n):
            for j in range(n):
                CM[i][j] = CM[i][j]/float(Degree[i])
                
        L = self.PowerMethod(CM, n, 0.2)
        normalizedL = self.normalize(L)
        
        for i in range(len(normalizedL)):
            score = normalizedL[i]
            sentence = sentences[i]
            sentence.setLexRankScore(score)
            
        return sentences

    def PowerMethod(self, CM, n, e):
        Po = numpy.array([1/float(n) for i in range(n)])
        t = 0
        delta = float('-inf')
        M = numpy.array(CM)
  
        while delta < e:
            t = t + 1
            M = M.transpose()
            P1 = numpy.dot(M, Po)
            diff = numpy.subtract(P1, Po)
            delta = numpy.linalg.norm(diff)
            Po = numpy.copy(P1)
            
        return list(Po)
    def buildMatrix(self, sentences):

        # build our matrix
        CM = [[0 for s in sentences] for s in sentences]
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                CM[i][j] = 0
        return CM
    def buildSummary(self, sentences, n):
        sentences = sorted(sentences,key=lambda x: x.getLexRankScore(), reverse=True)
        summary = []
        # sum_len = 0

        # while sum_len < n:
        #     summary += [sentences[i]]
        #     sum_len += len(sentences[i].getStemmedWords())

        for i in range(n):
            summary += [sentences[i]]
        return summary

    def normalize(self, numbers):
        max_number = max(numbers)
        normalized_numbers = []
        
        for number in numbers:
            normalized_numbers.append(number/max_number)
            
        return normalized_numbers
    def main(self, n, path):
        sentences  = self.text.openDirectory(path)
        idfs = self.sim.IDFs(sentences)
        CM = self.buildMatrix(sentences)
    
        sentences = self.score(sentences, idfs,CM, 0.1)

        summary = self.buildSummary(sentences, n)

        return summary


class sentence(object):
    
    def __init__(self, docName, stemmedWords, OGwords):
        
        self.stemmedWords = stemmedWords
        self.docName = docName
        self.OGwords = OGwords
        self.wordFrequencies = self.sentenceWordFreqs()
        self.lexRankScore = None

    def getStemmedWords(self):
        return self.stemmedWords

    def getDocName(self):
        return self.docName
    
    def getOGwords(self):
        return self.OGwords

    def getWordFreqs(self):
        return self.wordFrequencies
    
    def getLexRankScore(self):
        return self.LexRankScore
    
    def setLexRankScore(self, score):
        self.LexRankScore = score
    def sentenceWordFreqs(self):
        wordFreqs = {}
        for word in self.stemmedWords:
            if word not in wordFreqs.keys():
                wordFreqs[word] = 1
            else:
                wordFreqs[word] = wordFreqs[word] + 1
                
        return wordFreqs

class Preprocessing(object):

    def processFile(self, file_path_and_name):
        try:

            f = open(file_path_and_name,'rb')
            text = f.read()
            
            # soup = BeautifulSoup(text,"html.parser")
            # text = soup.getText()
            # text = re.sub("APW19981212.0848","",text)
            # text = re.sub("APW19981129.0668","",text)
            # text = re.sub("NEWSWIRE","",text)
            text_1 = re.search(r"<TEXT>.*</TEXT>",text, re.DOTALL)
            text_1 = re.sub("<TEXT>\n","",text_1.group(0))
            text_1 = re.sub("\n</TEXT>","",text_1)

            # replace all types of quotations by normal quotes
            text_1 = re.sub("\n"," ",text_1)
            text_1 = re.sub(" +"," ",text_1)
            # text_1 = re.sub("\'\'","\"",text_1)
            # text_1 = re.sub("\`\`","\"",text_1)


            sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                
            lines = sent_tokenizer.tokenize(text_1.strip())
            text_1 = lines

            sentences = []
            porter = nltk.PorterStemmer()
            
            for sent in lines:
                OG_sent = sent[:]
                sent = sent.strip().lower()
                line = nltk.word_tokenize(sent)
            
                stemmed_sentence = [porter.stem(word) for word in line]
                stemmed_sentence = filter(lambda x: x!='.'and x!='`'and x!=','and x!='?'and x!="'"
                                    and x!='!' and x!='''"''' and x!="''" and x!="'s", stemmed_sentence)
                if stemmed_sentence != []:
                    sentences.append(sentence(file_path_and_name, stemmed_sentence, OG_sent))
            
            return sentences

        
        except IOError:
            print 'Oops! File not found',file_path_and_name
            return [sentence(file_path_and_name, [],[])]

    
    def use_full_names(self, doc):
        names = self.getNames(doc)
        
        for i in range(len(doc)):
            doc[i] = self.getLongName(doc[i], names)
        return doc
        
    def getNames(self, doc):

        doc = ' '.join(doc).split()
        
      
        tags = st.tag(doc)
        doc = ' '.join(doc)

        names = []

        flag1 = False 

        for i in range(1, len(tags)):
            tag1 = tags[i-1]
            tag2 = tags[i]
            
            if i+1 < len(tags):
                tag3 = tags[i+1]
                if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and tag3[1] =='PERSON':
                    name = tag1[0] + ' ' + tag2[0] + ' ' + tag3[0]
                    if doc.find(name) > -1:
                        names.append(name)
                        i = i + 3
                        flag1 = True

            if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and not flag1 and i<len(tags):
                name = tag1[0] + ' ' + tag2[0]
                if doc.find(name) > -1:
                    names.append(name)
                    i = i + 2
                else:
                    i = i + 1
        return names

    def getLongName(self, sentence, names):
        sentence = sentence.split(" ")
        
        i = 0
        while i < len(sentence):
            word1 = sentence[i]
            for name in names:
                flag = False


                if i+1 != len(sentence):
                    word2 = sentence[i+1]
                    _2words = word1 + ' ' + word2
                    if self.begins_or_ends_with(_2words, name) and _2words != name:
                        if i == len(sentence)-2:
                            print sentence[i-1] + ' ' +_2words, name
                            sentence[i] = name
                            sentence = sentence[:i] + [name]
                            flag = True
                           
                        else:
                            temp = _2words + ' ' + sentence[i+2]
                            if temp != name and temp[:len(temp)-1] != name:
                                sentence = sentence[:i] + [name] + sentence[i+2:]
                                flag = True
                                
            # check one word at a time
                if self.begins_or_ends_with(word1, name) and not flag:
                    if i == len(sentence)-1:
                        sentence[i] = name
                       
                    else:
                        if sentence[i+1] != name.split(" ")[1]:
                            sentence[i] = name
            i +=1          
                        
        return ' '.join(sentence)

    
    def begins_or_ends_with(self, word, name):
        return name[:len(word)] == word or name[len(name)-len(word):] == word

    def get_file_path(self, file_name):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == file_name:
                    return os.path.join(root,name)
        print "Error! file was not found!!"
        return ""
    
    def get_all_files(self, path = None):
        retval = []
        

        if path == None:
            path = os.getcwd()

        for root, dirs, files in os.walk(path):
            for name in files:
                retval.append(os.path.join(root,name))
        return retval

    def openDirectory(self, path=None):
        file_paths = self.get_all_files(path)
        sentences = []
        for file_path in file_paths:
            sentences = sentences + self.processFile(file_path)
            
        return sentences


class DocumentSim(object):
    def __init__(self):
        self.text = Preprocessing()
    def TFs(self, sentences):

        tfs = {}
        for sent in sentences:
            wordFreqs = sent.getWordFreqs()
            
            for word in wordFreqs.keys():
                if tfs.get(word, 0) != 0:
                    tfs[word] = tfs[word] + wordFreqs[word]
                else:
                    tfs[word] = wordFreqs[word]
        return tfs
            
            
    def TFw(self, word, sentence):
        return sentence.getWordFreqs().get(word, 0)

    def IDFs(self, sentences):
        
        N = len(sentences)
        idf = 0
        idfs = {}
        words = {}
        w2 = []
        
        for sent in sentences:
            for word in sent.getStemmedWords():
                if sent.getWordFreqs().get(word, 0) != 0:
                    words[word] = words.get(word, 0)+ 1
                    
                    
        for word in words:
            n = words[word]
            try:
                w2.append(n)
                idf = math.log10(float(N)/n)
            except ZeroDivisionError:
                idf = 0
                    
            idfs[word] = idf
                
        return idfs

    def IDF(self, word, idfs):
        return idfs[word]



    def sim(self, sentence1, sentence2, idfs):
        
        numerator = 0
        denom1 = 0
        denom2 = 0

        for word in sentence2.getStemmedWords():
            numerator += self.TFw(word, sentence2) * self.TFw(word, sentence1) * self.IDF(word, idfs) ** 2

        
        for word in sentence1.getStemmedWords():
            denom2 += (self.TFw(word, sentence1) * self.IDF(word, idfs)) ** 2
                
        for word in sentence2.getStemmedWords():
            denom1 += (self.TFw(word, sentence2) * self.IDF(word, idfs)) ** 2

         
        try:
            return numerator / (math.sqrt(denom1) * math.sqrt(denom2))
        
        except ZeroDivisionError:
            return float("-inf")


if __name__=='__main__':
    
    lexRank = LexRank()
    doc_folders = os.walk("Documents").next()[1]
    total_summary = []
    for i in range(len(doc_folders)):
        path = os.path.join("Documents", '') + doc_folders[i]
        doc_summary = []        
        summary_length = 6                                                                                                                                                                                                                                                                                                                                                                                                                                              
        summary = []
        summary = lexRank.main(summary_length, path)
        print i
        for sentences in summary:
            # print "\n", sentences.getOGwords(), "\n"
            text_append =re.sub("\n","",sentences.getOGwords())
            # text_append = text_append.strip("'")
            text_append = text_append + " "
            doc_summary.append(text_append)
        total_summary.append(doc_summary)
    os.chdir("Lexrank_results")
    for i in range(len(doc_folders)):
        myfile = doc_folders[i]+".LexRank"
        f = open(myfile,'w')
        for j in range(summary_length):
            f.write(total_summary[i][j])
        f.close()

        
        
    
        
                
