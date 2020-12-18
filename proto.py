import os
import sys
import re
from git import Repo

#returns a recursive list with all the files and sub-files inside a folder
#Ex.:
#Folder1
#   |  |_________
#   |			|
#	Folder2     File3
#   |     |     
#   File1 File2  
#
#result = ["File1","File2","File3"]
def listFiles(path):
    
    entries = os.listdir(path) #current files and sub-folders at the path
    result = []
    
    for x in entries:
	        
        newPath = path+"/"+x

        if os.path.isdir(newPath):
            result += listFiles(newPath)

        else: 
            result.append(x)

    return result

def listJavaFiles(filesArray):

    resultat = []

    for file in filesArray:
        if ".java" in file:
            resultat.append(file)
    return resultat

def iterateVersions(url,path):

    text = "Version,Class\n"
    tempPath = path+"/temp"

    print("Cloning repository...")
    repo = Repo.clone_from(url, tempPath)
    print("DONE")

    print("Getting versions...")
    versionsList = repo.git.rev_list('MASTER').split("\n")
    versionsList = versionsList[0:10]
    print("DONE")

    print("Calculating metrics...")
    for hexVersion in versionsList:
        repo.git.reset('--hard',hexVersion)
        text += iterateClasses(hexVersion,tempPath)
    print("DONE")

    return text

def iterateClasses(version,tempPath):

    resultat = ""
    classList = listJavaFiles(listFiles(tempPath))

    for javaClass in classList:
        resultat += classMetrics(version,javaClass) + "\n"

    return resultat

def createCSV(text,path):

    print("Building CSV file...")
    csv = open("metrics.csv", "w")
    csv.write(text)
    csv.close()
    print("DONE")
        
#TODO
def classMetrics(version,javaClass):

    resultat = ""+version+","+javaClass
    return resultat





if __name__ == "__main__":

    #target = sys.argv[1]
    #list = listFiles(target)
    #result = listJavaFiles(list)

    url = sys.argv[1]
    path = sys.argv[2]

    text = iterateVersions(url,path)
    createCSV(text,path)

    print("Proto finished with success!\nThe 'metrics.csv' file has been saved at "+path)