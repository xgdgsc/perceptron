#!/usr/bin/python2
# -*- coding: utf-8 -*-
import argparse,glob,os

totalIndexNum=20760

def trainPerceptron(trainList,alpha,cycle):
    w=[0]*totalIndexNum
    for time in range(0,cycle):
        for doc in trainList:
            p=0
            for feature in doc[1]:
                p+=w[int(feature)-1]*float(doc[1][feature])
            y=1
            if doc[0]=='-1':
                y=-1
            if y*p<=0:
                for feature in doc[1]:
                    w[int(feature)-1]+=alpha*y*float(doc[1][feature])
    return w



def featureFileToList(filename):
    f=open(filename,'r')
    content=f.readlines()
    featureList=[]
    for lines in content:
        tokens=lines.split(' ')
        featureDict={}
        docList=[]
        docList.append(tokens[0])
        for feature in tokens[1:-1]:
            kv=feature.split(':')
            #print kv
            featureDict[kv[0]]=kv[1]
        docList.append(featureDict)
        featureList.append(docList)
    return featureList





if __name__=="__main__":
    parser = argparse.ArgumentParser("Training routine, output weights")
    parser.add_argument('-i','--in_file',help='Input file path',required=True)
    parser.add_argument('-o','--out_file',help='Output file path',required=True)
    args=parser.parse_args()
    #    groupFileList=glob.glob(os.path.join(args.in_folder,'group*'))
    #print groupFileList
    featureList=featureFileToList(args.in_file)
    w=trainPerceptron(featureList,0.25,50)
    with open(args.out_file,'w') as outfile:
        for weight in w:
            outfile.write(str(weight)+'\n')
