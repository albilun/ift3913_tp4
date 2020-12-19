import os
import sys
import shutil
from git import Repo
import subprocess
import statistics

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

#Takes an array of files and returns an array of only .java files
def listJavaFiles(filesArray):

    resultat = []

    for file in filesArray:
        if ".java" in file:
            resultat.append(file)
    return resultat

#Clones the repository at path/temp
#Then iterates between versions and calls classMetrics()
#Returns a String that will be saved as .csv by createCSV()
def iterateVersions(url,path):

    text = "id_version,n_classes,m_c_BC\n"
    tempPath = path+"\\temp"

    print("Cloning repository...")

    try:
        repo = Repo.clone_from(url, tempPath)
    except:
    	print("ERROR: The path is not empty!")
    	sys.exit()

    print("DONE")

    print("Getting versions...")
    versionsList = repo.git.rev_list('MASTER').split("\n")
    percentage = int(len(versionsList)/10) 
    versionsList = versionsList[0:percentage] #looking at the last 10% versions
    print("DONE")

    print("Calculating metrics...")

    iteration = 1
    totalIterations = len(versionsList)
    for hexVersion in versionsList:
        
        print(str(iteration)+"/"+str(totalIterations)) 
        repo.git.reset('--hard',hexVersion)
        text += classMetrics(hexVersion,tempPath)
        iteration += 1

    print("DONE")

    repo.index.remove(tempPath,True,r=True)

    return text

#Uses tp1.jar to write the metrics of each version
def classMetrics(version,tempPath):

    resultat = ""
    classList = listJavaFiles(listFiles(tempPath))
    subprocess.call(['java', '-jar', 'tp1.jar', 'temp'])

    median = analyseJavaCSV(version,tempPath+"/classes.csv")
    resultat = version+","+str(len(classList))+","+median+"\n"

    os.remove(tempPath+"/classes.csv")
    os.remove(tempPath+"/methods.csv")

    return resultat

#calculates the median from classes.csv
def analyseJavaCSV(version,path):
    
    fileReader = open(path)
    fileReader.readline()
    classes_BC = []

    for line in fileReader:
        temp = line.split(",")
        temp = temp[6]
        
        if "\n" in temp:
            temp = temp.split("\n")[0]

        classes_BC.append(temp)

    fileReader.close()
    median = statistics.median(classes_BC)

    return median


#Creates mertic.csv from text
def createCSV(text,path):

    print("Building CSV file...")
    csv = open("metrics.csv", "w")
    csv.write(text)
    csv.close()
    print("DONE")

#Cleans all the downloaded files
def cleanTemp(path):
    
    print("Cleaning up...")
    try:
        os.rmdir(path)
        print("DONE")
    except:
        print("WARNING: Cleaning was unsuccessful")
 

if __name__ == "__main__":

    url = sys.argv[1]
    path = sys.argv[2]

    text = iterateVersions(url,path)
    createCSV(text,path)
    cleanTemp(path+"\\temp")

    print("Proto finished with success!\nThe 'metrics.csv' file has been saved at "+path)