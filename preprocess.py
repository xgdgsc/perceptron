#!/usr/bin/python2
# -*- coding: utf-8 -*-

import argparse,nltk,os,string,cPickle,math
from nltk.corpus import stopwords

def preprocess(ifolder):
    filelist=os.listdir(ifolder)
    docs=[]
    for filename in filelist:
        f=open(os.path.join(ifolder,filename),'r')
        raw=f.read()
        #remove punctuation
        no_punctuation_raw=raw.translate(string.maketrans("",""),string.punctuation)
        tokens=nltk.word_tokenize(no_punctuation_raw)
        words = [w.lower() for w in tokens]

        #remove stop words
        no_stop_words = [w for w in words if not w in stopwords.words('english')]
        myStemmer = nltk.stem.lancaster.LancasterStemmer()
        stemmed_words=[myStemmer.stem(word) for word in no_stop_words]
        docs.append(stemmed_words)
    return docs

def featureExtraction(docs1,docs2):
    totalIndex={}
    index=1

    # prepare total dictionary and prepare idf
    for doc in docs1:
        # ignore dup in single doc to calculate idf
        docSet=set(doc)
        #print str(len(doc)-len(docSet))
        for word in docSet:
            if word not in totalIndex:
                totalIndex[word]=[index,1]
                index+=1
            else:
                totalIndex[word][1]+=1

    for doc in docs2:
        docSet=set(doc)
        for word in docSet:
            if word not in totalIndex:
                totalIndex[word]=[index,1]
                index+=1
            else:
                totalIndex[word][1]+=1

    index-=1
    totalDictLength=index
    totalDocNumber=len(docs1)+len(docs2)
    totalNumIndex={}
    for key in totalIndex:
        totalNumIndex[totalIndex[key][0]]=totalIndex[key][1]

    #print totalNumIndex
    print "Index: "+str(index)
    print "Len of totalIndex:"+str(len(totalIndex))
    print "Total doc number:"+str(totalDocNumber)

    # calculate tf,tfidf and generate feature vector
    doc1FeatureList=[]
    for doc in docs1:
        wordDict={}
        for word in doc:
            if totalIndex[word][0] not in wordDict:
                wordDict[totalIndex[word][0]]=1
            else:
                wordDict[totalIndex[word][0]]+=1
        #calc tfidf as feature vector
        docFeatureDict={}
        for key in wordDict:
            tfidf=wordDict[key]*math.log(totalDocNumber/totalNumIndex[key])
            docFeatureDict[key]=tfidf
        doc1FeatureList.append(docFeatureDict)

    doc2FeatureList=[]
    for doc in docs2:
        wordDict={}
        for word in doc:
            if totalIndex[word][0] not in wordDict:
                wordDict[totalIndex[word][0]]=1
            else:
                wordDict[totalIndex[word][0]]+=1
        #calc tfidf as feature vector
        docFeatureDict={}
        for key in wordDict:
            tfidf=wordDict[key]*math.log(totalDocNumber/totalNumIndex[key])
            docFeatureDict[key]=tfidf
        doc2FeatureList.append(docFeatureDict)
        #print doc1FeatureList
    print len(doc1FeatureList)
    print len(doc2FeatureList)

    return [doc1FeatureList,doc2FeatureList]

if __name__=="__main__":
    parser = argparse.ArgumentParser("Preprocessing routine.")
    parser.add_argument('-i1','--input_folder_1',help='Input data path 1',required=True)
    parser.add_argument('-i2','--input_folder_2',help='Input data path 2',required=True)
    parser.add_argument('-o','--output_folder',help='Output folder name',required=True)
    args=parser.parse_args()

    if not os.path.exists(args.output_folder):
        try:
            os.makedirs(args.output_folder)
        except OSError,why:
            print "Failed: %s"%str(why)

    docs1=preprocess(args.input_folder_1)
    docs2=preprocess(args.input_folder_2)
    # cPickle.dump(docs1,open(os.path.join(args.output_folder,"docs1.pk"),'wb'))
    # cPickle.dump(docs2,open(os.path.join(args.output_folder,"docs2.pk"),'wb'))

    #docs1=cPickle.load(open(os.path.join(args.output_folder,"docs1.pk")))
    #docs2=cPickle.load(open(os.path.join(args.output_folder,"docs2.pk")))
    print len(docs1)
    print len(docs2)
    featureVectors=featureExtraction(docs1,docs2)
    print len(featureVectors)
    
    #write to file
    with open(os.path.join(args.output_folder,"feature.f"),'w') as outfile:
        for fVector in featureVectors[0]:
            outfile.write("+1 ")
            for feature in fVector:
                outfile.write(str(feature)+':'+str(fVector[feature])+' ')
            outfile.write('\n')

        for fVector in featureVectors[1]:
            outfile.write("-1 ")
            for feature in fVector:
                outfile.write(str(feature)+':'+str(fVector[feature])+' ')
            outfile.write('\n')
