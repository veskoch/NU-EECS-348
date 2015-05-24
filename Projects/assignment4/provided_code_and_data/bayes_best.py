# Name: Andrew Kluge (ajk386), Vesko Cholakov (vgc917), Sophia Lou (sll411), Richard Gates Porter (rgp633)
# Date: May 22, 2015
# Description: Better Bayes Classifier, using positive and negative dictionaries with unigrams and bigrams
#
#

import math, os, pickle, re

class Best_Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      # If the dictionaries exist, load them
      if (os.path.isfile("BigramsPositive") and os.path.isfile("BigramsNegative")):
         self.positiveBigrams = self.load("BigramsPositive")
         self.negativeBigrams = self.load("BigramsNegative")
         print "The Bigram dictionaries exist and won't be recalculated."
      else: 
         print "No existing Bigram dictionaries found."
         self.positiveBigrams = {}
         self.negativeBigrams = {}
         self.trainBigrams()
         print "Bigram dictionaries generated."
      if (os.path.isfile("positive") and os.path.isfile("negative")):
         self.positiveUnigrams = self.load("positive")
         self.negativeUnigrams = self.load("negative")
         print "The unigram dictionaries exist and won't be recalculated" 
      else:
         print "No existing Unigram dictionaries found." 
         self.positiveUnigrams = {}
         self.negativeUnigrams = {}
         self.trainUnigrams()
         print "The bigram dictionaries exist and won't be recalculated" 

   def trainBigrams(self):   # train for bigrams 
      """Trains the Naive Bayes Sentiment Classifier."""

      # Create a list IFileList which contains the file names of all movie reviews
      IFileList = []
      for fileObj in os.walk("movies_reviews/"):
         IFileList = fileObj[2]
         break

      # For each file
      for fileName in IFileList: 

         def updateFrequency(dictionary, word):
            """ Increments the frequency of the provided word in the provided dictionary. """
            # If word is alrady in dictionary, increment
            if (dictionary.has_key(word)):   
               dictionary[word] += 1
            else: # If not, initialize count to 1
               dictionary[word] = 1

         # Load content of review
         content = self.loadFile("movies_reviews/" + fileName)
         # Tokenize content
         a, tokenized = self.tokenize(content)

         # Determine the mood of the review.
         for word in tokenized:
            if (fileName[7] == "1"):
               updateFrequency(self.negativeBigrams, word)
            elif (fileName[7] == "5"):
               updateFrequency(self.positiveBigrams, word)

      # Save the dictionaries to disk
      self.save(self.negativeBigrams, "BigramsNegative")
      self.save(self.positiveBigrams, "BigramsPositive")

   def trainUnigrams(self):   # trains for Unigrams 
      """Trains the Naive Bayes Sentiment Classifier."""

      # Create a list IFileList which contains the file names of all movie reviews
      IFileList = []
      for fileObj in os.walk("movies_reviews/"):
         IFileList = fileObj[2]
         break

      # For each file
      for fileName in IFileList: 

         def updateFrequency(dictionary, word):
            """ Increments the frequency of the provided word in the provided dictionary. """
            # If word is alrady in dictionary, increment
            if (dictionary.has_key(word)):   
               dictionary[word] += 1
            else: # If not, initialize count to 1
               dictionary[word] = 1

         # Load content of review
         content = self.loadFile("movies_reviews/" + fileName)
         # Tokenize content
         tokenized, b = self.tokenize(content)

         # Determine the mood of the review.
         for word in tokenized:
            if (fileName[7] == "1"):
               updateFrequency(self.negativeUnigrams, word)
            elif (fileName[7] == "5"):
               updateFrequency(self.positiveUnigrams, word)

      # Save the dictionaries to disk
      self.save(self.negativeUnigrams, "negative")
      self.save(self.positiveUnigrams, "positive")
         
    
   def classify(self, sText):
      """Given a target string sText, the function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

      negative_probability = 0
      positive_probability = 0 

      # Tokenize sText
      unigrams, bigrams = self.tokenize(sText)

      # Get a list of all values in a dictionay
      pos_uni = self.positiveUnigrams.values()
      neg_uni = self.negativeUnigrams.values()
      pos_bi = self.positiveBigrams.values()
      neg_bi = self.negativeBigrams.values()

      # Totals word in a dictionary 
      total_words_in_positiveUni = sum(pos_uni)
      total_words_in_negativeUni = sum(neg_uni)
      total_words_in_positiveBi = sum(pos_bi)
      total_words_in_negativeBi = sum(neg_bi)  

      # Run Bayes Classifier for Unigrams 

      i = 0
      j = 0
      
      for word in unigrams:   # For each word in sText  
         if (self.positiveUnigrams.has_key(word)):  # Is word in positive dict?
            positive_probability += math.log(((self.positiveUnigrams[word] + 1.0) / total_words_in_positiveUni))
            i += 1
         if (self.negativeUnigrams.has_key(word)):  # Is word in negative dict?
            negative_probability += math.log(((self.negativeUnigrams[word] + 1.0) / total_words_in_negativeUni))
            j += 1

      if i == 0:
         i = 1
      if j == 0:
         j = 1 

      positive_probability = positive_probability / i
      negative_probability = negative_probability / j

      # Run Bayes Classifier for Bigrams
      m = 0
      n = 0 
      pos_prob = 0
      neg_prob = 0 

      for word in bigrams: # for each pair of words 
         if (self.positiveBigrams.has_key(word)):
            pos_prob += math.log(((self.positiveBigrams[word] + 1.0) / total_words_in_positiveBi))
            m += 1
         if (self.negativeBigrams.has_key(word)):
            neg_prob += math.log(((self.negativeBigrams[word] + 1.0) / total_words_in_negativeBi))
            n += 1 

      if m == 0:
         m = 1
      if n == 0:
         n = 1

      positive_probability += (pos_prob / m)
      negative_probability += (neg_prob / n)

      diff = positive_probability - negative_probability 

      print diff

      if math.fabs(diff) <= 0.1: 
         return "neutral"
      if diff > 0: 
         return "positive"
      else: 
         return "negative"


   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""
      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""
      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      uniTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               uniTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               uniTokens.append(str(c.strip()))
               
      if sToken != "":
         uniTokens.append(sToken)

      biTokens = []

      for y in range(len(uniTokens) - 1):
         a = uniTokens[y]
         b = uniTokens[y + 1]
         biTokens.append(a + ' ' + b)

      return uniTokens, biTokens 
