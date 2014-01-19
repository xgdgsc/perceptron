#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import division
import argparse,glob,os,cPickle
from train import *



def classifyPerceptron(feature,w):
    p=0
    y=0
    for key in feature:
        p+=w[int(key)-1]*float(feature[key])
    if p<=0:
        y=-1
    else:
        y=1
    return y


def precision(tp,fp):
    return tp/(tp+fp)

def recall(tp,fn):
    return tp/(tp+fn)

def accuracy(tp,fp,fn,tn):
    return (tp+tn)/(tp+tn+fp+fn)

def f1(precision,recall):
    return 2*precision*recall/(precision+recall)

def test(trainSet,testSet):
    w=trainPerceptron(trainSet,0.2,50)
    #f=open("/tmp/weight.w",'wb')
    #cPickle.dump(w,f)
    #f.close()
    #w=cPickle.load(open("/tmp/weight.w",'rb'))
    tp=fp=fn=tn=0
    for item in testSet:
        y=classifyPerceptron(item[1],w)
        #print item[0]
        if y==1 and item[0]=='+1':
            tp+=1
        elif y==1 and item[0]=='-1':
            fp+=1
        elif y==-1 and item[0]=='+1':
            fn+=1
        elif y==-1 and item[0]=='-1':
            tn+=1

    prec=precision(tp,fp)
    rec=recall(tp,fn)
    accu=accuracy(tp,fp,fn,tn)
    fscore=f1(prec,rec)

    return [prec,rec,accu,fscore]






if __name__=="__main__":
    parser = argparse.ArgumentParser("Training routine, output weights")
    parser.add_argument('-i','--in_path',help='Input group file path',required=True)
    parser.add_argument('-o','--out_file',help='Output file path',required=False)
    args=parser.parse_args()
    groupFileList=glob.glob(os.path.join(args.in_path,'group*'))
    featureGroupList=[]
    for filename in groupFileList:
        featureGroup=featureFileToList(filename)
        featureGroupList.append(featureGroup)
    #print len(featureGroupList)
    #print featureGroupList[0][0]
    #w=trainPerceptron(featureGroupList[2],0.25,500)
    #print classifyPerceptron(featureGroupList[0][0][1],w)
    results=[]
    for i in range(0,5):
        testSet=featureGroupList[i]
        trainSet=[]
        for j in range(0,5):
            if j!=i:
                trainSet+=featureGroupList[j]
        #print len(testSet)
        #print len(trainSet)
        print "Round "+str(i+1)+" ..."
        resi=test(trainSet,testSet)
        results.append(resi)
    print results
    sum=[0]*4
    for item in results:
        for i in range(0,4):
            sum[i]+=item[i]
    average=map(lambda x:x/5,sum)
    print average

    with open(args.out_file,'w') as outfile:
        outfile.write("\t\tPrecision\t\tRecall\t\tAccuracy\t\tF1Score\n")
        round=1
        for res in results:
            outfile.write("Round"+str(round))
            round+=1
            for item in res:
                outfile.write("\t"+str(item))
            outfile.write('\n')
        outfile.write("Average")
        for item in average:
            outfile.write("\t"+str(item))
