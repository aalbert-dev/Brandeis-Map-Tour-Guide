# @author arjunalbert@brandeis.edu
# Method to return the most frequent words from N Documents
# < word1 >
# < word1, word2 >
# < word1, word2, word3 >
# where wordN is the Nth most frequent word
# Assume documents is a list of strings representing each document
def wordFrequency(documents):

    # dictionary where key = "word" and value = number of occurances
    wordToFreq = {} 
   
    for document in documents:
        words = document.split(" ")

        # for each word in each document 
        for word in words: 

            # increment frequency for every occurance
            # or set first occurance
            if word in map(lambda x: x[1], wordToFreq):
                wordToFreq[word] = wordToFreq[word] + 1
            else:
                wordToFreq[word] = 1

    # {key: value for key, value in word to frequency dictionary 
    # sorted by their values which are frequency in a decreasing order}
    wordToFreqDescending = {k: v for k, v in sorted(wordToFreq.items(), key=lambda x: x[1])[::-1]} 

    # the tuple of tuples where wordToFreqDescending[N] is the Nth most frequency word from the documents
    return ((wordToFreqDescending[0]), 
           (wordToFreqDescending[0], wordToFreqDescending[1]), 
           (wordToFreqDescending[0], wordToFreqDescending[1], wordToFreqDescending[2]))