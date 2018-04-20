"""
Below is the HomeWork Assignment 1.
To run the script type the below command in command prompt/terminal
python IRHW1.py "path_to_transcripts_folder"
"""
#importing necessary modules

import pandas as pd
import glob
import re
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math
import sys

#code to tak user input
user_input = sys.argv[1]
data_path= user_input + '*.txt'

file_path=[]
data=[]
doc_data=[]
data_wout_stop=[]
stemmer = PorterStemmer()
stemmed_word=[]

#setting the stopword 
stop_words= set(stopwords.words('english'))

#function to read the transcripts files from folder
#returns two list one with combine list of all the words
#second with words per document
def reading_file(data_path):
    
    for i in glob.glob(data_path):
        file_path.append(i)
    
    for i in file_path:
        filereader = open(i,"rt")
        line = filereader.read()
        #line = line.replace("<br />", " ")
        #line  =re.sub("[^a-zA-Z]"," ",line)
        
        line = re.sub("[^A-Za-z0-9]+"," ",line) #removal of special characters
        line = line.lower()
        doc_data.append(word_tokenize(line)) #creating word tokens
        data.extend(word_tokenize(line))
    
    return data,doc_data

data,doc_data = reading_file(data_path)

#function to reomove stop words
def stop_word_removal(data):
    for i in data:
        if i not in stop_words:
            data_wout_stop.append(i) 
    return data_wout_stop

# function to do stemming
def stemming(data_wout_stop):
    for i in data_wout_stop:
        stemmed_word.append(stemmer.stem(i))
    return stemmed_word

data_wout_stop = stop_word_removal(data)
stemmed_word=stemming(data_wout_stop)

print("Number of word token in database: ", len(stemmed_word))
print("\n")
print("Number of unique words: ", len(list(set(stemmed_word))))
print("\n")
print("Number of words that occur only once")
word_count=Counter(stemmed_word)
word_count=pd.Series(word_count)
word_count=pd.DataFrame(word_count)
word_count.columns = ['count']
print(len(word_count[word_count['count']==1]))
print("\n")
print("Average number of words per document: ", round(len(word_count)/404,2))
print("For top 30 words below are the calculation\n")

#creating the table for top 30 words
df = pd.DataFrame(Counter(stemmed_word).most_common(30))
df.columns = ['word','Word_Count']

word_list_30 = list(df.word)
df=pd.concat([df]*404)

doc_data_stemmed=[]
temp=[]
#stemming words per document
for k in doc_data:
    for l in k:
        temp.append(stemmer.stem(l))
    doc_data_stemmed.append(temp)
    temp=[]

doc_data_stemmed_count=[]
#counting words per document
for c in doc_data_stemmed:
    doc_data_stemmed_count.append(Counter(c))


doc_no=[]
doc_word=[]
doc_word_count=[]
c=0
#for top 30 words calculating term frequency per document
for i in doc_data_stemmed_count:
    for j in word_list_30:
        doc_no.append(c)
        doc_word.append(j)
        doc_word_count.append(i[j])
     
    c=c+1
dft=[]
#for top 30 words calculating DFT 
for i in word_list_30:
    c=0
    for j in doc_data_stemmed:
        if i in j:
            c=c+1
    dft.append(c)
#creating final table    
df['Doc_no']=doc_no
df['N']=404
df['TF']=doc_word_count
df['DFT']=dft*404
df['N/DFT']=df['N']/df['DFT']
idf=[]
for m in df['N/DFT']:
    idf.append(math.log2(m))
   
df['IDF']=idf
df['TF*IDF']=df['TF']*df['IDF']
df['Probabilities'] = df['TF']/len(stemmed_word)
print(df)
