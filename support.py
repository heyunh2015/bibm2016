# -*- coding: utf-8 -*- 
import os,re,operator
SystemPathSeperator = '\\'

def saveFile(string, fileName):
    fp_w = open(fileName,'w')
    fp_w.write(string)        
    fp_w.close()
    return 0

def listDir(path):
    list = []
    for file in os.listdir(path):  
        if os.path.isdir(os.path.join(path, file)):  # dir 
            list.extend(listDir(os.path.join(path, file)))
        else:  # file
            list.append(os.path.join(path, file))
    return list

def sampleEvalOnFolder(evaluateTool, qrelFile, resultFiles, evalFiles):
    files = listDir(resultFiles)
    
    for file in files:
        filename = file[file.rfind(SystemPathSeperator) + 1:]
        cmdStr = evaluateTool + SystemPathSeperator + 'sample_eval.pl -q ' + qrelFile + ' ' + resultFiles + SystemPathSeperator + filename + ' > ' + evalFiles + SystemPathSeperator + filename + '.eval'
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0

def printDict(dict, levelNumber):
    if levelNumber == 1:
        for i in dict:
            print i, dict[i]
    elif levelNumber == 2:
        for i in dict:
            for j in dict[i]:
                print i,j,dict[i][j]
                
def removePunctuation(text):
    r='[��!"#$%&\'()*+,.��/:;<=>?@[\\]^_`{|}~]+'
    text = re.sub(r,'',text)
    text = re.sub('  ',' ',text)
    text = re.sub('-',' ',text)
    text = re.sub('—',' ',text)
    text = re.sub('·','',text)
    text = re.sub('•','',text)
    return text

def loadStopWord():
    stopWordsDic = {}
    fp = open('I:\\bibm2016\\experiments\\english.stop')
    for line in fp.readlines():
        stopWord = line.strip()
        if stopWord not in stopWordsDic:
            stopWordsDic[stopWord] = 1
    return stopWordsDic

def isNotStopWords(word, stopWordsDic):
    if word in stopWordsDic:
        return False
    else:
        return True 

def loadMeshTerms(field):
    if field=='disease':
        meshClass = 'C'
        meshTermFile = 'I:\\bibm2016\\experiments\\mesh\\mtrees2015.bin'
        meshTermsDict = {}
        fp = open(meshTermFile)
        for line in fp.readlines():
            lineArr = line.strip().split(';')
            if lineArr[1][0]==meshClass:
                meshTerm = removePunctuation(lineArr[0])
                meshTermLower = ''
                meshTermList = meshTerm.strip().split(' ')
                for term in meshTermList:
                    meshTermLower += term.lower()+' '
                meshTermLower = meshTermLower.strip()
                if meshTermLower not in meshTermsDict:
                    meshTermsDict[meshTermLower] = lineArr[1].strip()
                    
    if field=='all':
        #meshClass = 'C'
        meshTermFile = 'I:\\bibm2016\\experiments\\mesh\\mtrees2015.bin'
        meshTermsDict = {}
        fp = open(meshTermFile)
        for line in fp.readlines():
            lineArr = line.strip().split(';')
            #if lineArr[1][0]==meshClass:
            meshTerm = removePunctuation(lineArr[0])
            meshTermLower = ''
            meshTermList = meshTerm.strip().split(' ')
            for term in meshTermList:
                meshTermLower += term.lower()+' '
            meshTermLower = meshTermLower.strip()
            if meshTermLower not in meshTermsDict:
                meshTermsDict[meshTermLower] = lineArr[1].strip()           
    return meshTermsDict

def loadMeshTermsSynonym(meshFile):
    meshTermSynonymDict = {}
    if meshFile=='disease':
        meshTermSynonymFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords_disease.txt'
    elif meshFile=='all':
        meshTermSynonymFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords.txt'
    fp = open(meshTermSynonymFile)
    for line in fp.readlines():
        lineArr = line.strip().split(':')
        meshTerm = removePunctuation(lineArr[0])
        if meshTerm not in meshTermSynonymDict:
            meshTermSynonymDict[meshTerm] = {}
        meshTermSynonymList = lineArr[1].strip('|').split('|')
        meshTermSynonymNumber = len(meshTermSynonymList)-1
        if meshTermSynonymNumber>0:
            for meshTermSynonymIndex in range(0, meshTermSynonymNumber+1):
                meshTermSynonym = removePunctuation(meshTermSynonymList[meshTermSynonymIndex])
                meshTermSynonymDict[meshTerm][meshTermSynonym] = 1
                
    #support.printDict(meshTermSynonymDict, 1)
    return meshTermSynonymDict

def sentenceLower(sentence):
    sentenceLowerConetent = ''
    sentenceWordsList = sentence.strip().split(' ')
    for word in sentenceWordsList:
        sentenceLowerConetent += word.lower() + ' '
    sentenceLowerConetent = sentenceLowerConetent.strip()
    return sentenceLowerConetent

def getResultFileNameFromFolder(folderName):
    filesNameList = listDir(folderName)
    return filesNameList

def getResultFileNameFromFile(folderName, resultNamesFile):
    SystemPathSeperator = '\\'
    filesNameList = []
    fp =open(resultNamesFile)
    for line in fp.readlines():
        filesNameList.append(folderName + SystemPathSeperator + str(line).strip())
    return filesNameList

def extractOriginalWords(originalQueryFile):
    originalWords = {}
    fp = open(originalQueryFile)
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[0]=='<num>':
            queryId = lineArr[2]
            originalWords[queryId] = []
        if len(lineArr)>4:
            querySentence = removePunctuation(str(line.strip()))
            queryWordList = querySentence.strip().split(' ')
            for word in queryWordList:
                originalWords[queryId].append(word)
    
    return originalWords


def storeweakClassArr(inputTree,filename):
    import pickle
    fw = open(filename,'wb')
    pickle.dump(inputTree, fw)
    fw.close()
 
def grabweakClassArr(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr) 

def rankDict(dict, keyOrValue):
    rankResult = ''
    rankIndex = 0
    for item in sorted(dict.iteritems(), key=operator.itemgetter(keyOrValue), reverse=True):
        rankResult += str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+'\n'
        rankIndex += 1
    return rankResult