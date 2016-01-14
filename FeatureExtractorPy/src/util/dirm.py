'''
Created on 2 Jul 2015
The module handles the directoy managment
@author: Coryn
'''
import os
currentOS = os.name

subSampleName = "Ss2"
subSample = "sub_sample2/"


winOutputDirectory = "F:/Coryn/Google Drive/Project/Data/"
awsOutputDirectory = "/home/ubuntu/Data/"
outputDirectory = ''

winOutputDatabaseName = "TurnerDbLocal"+subSampleName
awsOutputDatabaseName = "TurnerDbAWS"+subSampleName
sqlite_file = ''


winRootDirectory = "F:/Coryn/Documents/Project_Images/Turner/"
awsRootDirectory = "/home/ubuntu/Data/Project_Images/Turner/"
rootDirectory = ''

    
if(currentOS=='nt'):
    outputDirectory = winOutputDirectory + subSample
    rootDirectory = winRootDirectory + subSample
    sqlite_file = outputDirectory + winOutputDatabaseName  + '.sqlite'
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    
if(currentOS=='posix'):
    outputDirectory = awsOutputDirectory + subSample
    rootDirectory = awsRootDirectory + subSample
    sqlite_file = outputDirectory + awsOutputDatabaseName + '.sqlite'
    curImgs = rootDirectory + subSample;
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    

print outputDirectory
print rootDirectory