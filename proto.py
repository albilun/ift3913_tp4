import os
import sys
import re

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

if __name__ == "__main__":

    target = sys.argv[1]
    list = listFiles(target)
    result = listJavaFiles(list)
    print(result)