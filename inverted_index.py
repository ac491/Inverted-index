from pprint import pprint
import os
from os import listdir
from os.path import isfile, join
import re
import json
import pickle

PATH = "C:/Users/Sneha/Desktop/python/documents"
WORDS =["record","band","member","single","singer","metal","rock","grammy","platinum","group"]

def getFiles():
    onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    return onlyfiles

def createIndex():

        inverted = {}
        fileList = getFiles()
        for word in WORDS:
                for file in fileList:
                        locations = inverted.setdefault(word, [])
                        if checkWord(word, PATH + "/" + file) == True:
                                locations.append(file)

        return inverted


def checkWord(word, filename):
        if word in (open(filename).read()).lower():
                return True
        else:
                return False


def writeIndex(inverted_index):
       json.dump(inverted_index, open("C:/Users/sneha/Desktop/python/index.txt", 'w'))

def readIndex():
        inverted_index = {}
        inverted_index = json.load(open("C:/Users/sneha/Desktop/python/index.txt"))
        return inverted_index

def writeList(list):
        with open("C:/Users/sneha/Desktop/python/config.txt", 'wb') as f:
                pickle.dump(list, f)

def readList():
        with open("C:/Users/sneha/Desktop/python/config.txt", 'rb') as f:
                list = pickle.load(f)
        return list

def getIndex():
        if os.stat("C:/Users/sneha/Desktop/python/index.txt").st_size == 0:
                inverted_index = createIndex()
                writeIndex(inverted_index)
        else:
                inverted_index = readIndex()

        if os.stat("C:/Users/sneha/Desktop/python/config.txt").st_size == 0:
                writeList(getFiles())
                return inverted_index
        else:
                originalFiles = set(readList())
                updatedFiles = set(getFiles())
                if len(updatedFiles - originalFiles) > 0:
                        newFiles = updatedFiles - originalFiles
                        #print(newFiles)
                        inverted_index = updateIndex(inverted_index, newFiles)
                        #pprint(inverted_index)
                        writeIndex(inverted_index)
                        writeList(getFiles())
                        return inverted_index

                else:
                        return inverted_index


def updateIndex(inverted_index, newFiles):
        for word in WORDS:
                for file in newFiles:
                        locations = inverted_index.setdefault(word, [])
                        if checkWord(word, PATH + "/" + file) == True:
                                locations.append(file)
        return inverted_index

def search(query):

        inverted_index = getIndex()
        result_set = set()
        operation = None
        for index, word in enumerate(re.split(" +(AND|OR) +",query)):
               
                if index == 0:
                        if word.find('NOT ') == 0:
                                realword = word[4:]
                                current_set = set(inverted_index.get(realword))
                                result_set = set(getFiles())
                                result_set -=current_set
                        else:        
                                result_set = set(inverted_index.get(word)) 
                        continue
                inverted = False 
                if word in ['AND','OR']:
                        operation = word
                        continue

                if word.find('NOT ') == 0:
                        if operation == 'OR':
                                continue
                        inverted = True
                        realword = word[4:]
                else:
                        realword = word

                if operation is not None:
                        current_set = set(inverted_index.get(realword))

                        if operation == "AND":
                                if inverted is True:
                                        result_set -= current_set
                                else:
                                        result_set &= current_set

                        elif operation == "OR":
                                result_set |= current_set

                        operation=None
        return sorted(result_set)


if __name__=="__main__":
        query = "single AND NOT singer"
        query = input("Enter search query: ")
        result = search(query)
        print("\nResults: \n")
        print(result)
        print("\n")