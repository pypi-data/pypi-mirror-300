import configparser
import os

def GetConfigValues(): 
    global PTProjectName 
    global PTTestsetName_ToCloneFrom
    global PT_Token
    global PT_API_BaseURL
    global PTTestsetName_New
        
    userInputs = configparser.ConfigParser()

    filename = "userInputs.ini"
    filepath = getFilePath(os.getcwd(),filename)
    #iniPath = os.path.join(os.getcwd(), 'userInputs.ini')
    userInputs.read(filepath)    
        
    PTProjectName = userInputs['UserInputs']['PractiTestProjectName']

    PTTestsetName_ToCloneFrom = userInputs['UserInputs']['PractiTestTestSetName_ToCloneFrom']

    PT_Token = userInputs['UserInputs']['PT_Token']
        
    PTTestsetName_New = userInputs['UserInputs']['PractiTestTestSetName_New']
   
def getFilePath(currentWorkingDirectory, filename):
    while True:
        potential_filePath = os.path.join(currentWorkingDirectory,filename)
        if os.path.isfile(potential_filePath):
            return potential_filePath
        parentDirectory = os.path.dirname(currentWorkingDirectory)
        if currentWorkingDirectory == parentDirectory:
            return None
        currentWorkingDirectory = parentDirectory 