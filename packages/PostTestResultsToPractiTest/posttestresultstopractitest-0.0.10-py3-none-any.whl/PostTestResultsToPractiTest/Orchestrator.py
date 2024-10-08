from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTTestSetId
from PostTestResultsToPractiTest import ClonePTTestSet
from PostTestResultsToPractiTest import CreatePTTestSet
from PostTestResultsToPractiTest import GetPTTest
from PostTestResultsToPractiTest import GetPTInstance
from PostTestResultsToPractiTest import CreatePTInstance
from PostTestResultsToPractiTest import PostTestResults
from PostTestResultsToPractiTest.EnumClass import TestResultStatus

global clonedTestSetId
 
def CreateTestSetProcess():
    try:
        GetConfigValues.GetConfigValues()
        
        testSetWeWantToCreate = GetPTTestSetId.RetrieveTestSetId(GetConfigValues.PTTestsetName_New)
        
        #if the test set we want to create is not already there, then create, otherwise re-use
        if testSetWeWantToCreate is None: 
            testSetIdToCloneFrom = GetPTTestSetId.RetrieveTestSetId(GetConfigValues.PTTestsetName_ToCloneFrom)
            if testSetIdToCloneFrom is not None:
                globals()['clonedTestSetId'] = ClonePTTestSet.ClonePTTestSet(testSetIdToCloneFrom)
                return clonedTestSetId
            else:
                raise Exception ("Test_set_to_clone_from is not valid")
        else:
            globals()['clonedTestSetId'] = testSetWeWantToCreate
            return clonedTestSetId
            
    except Exception as msg:
        print ("Something went wrong in CreateTestSetProcess(): ", msg)
        raise Exception (msg)

def CreateTestSetFromFeature(featureFileName: str, releaseVersion: str, customFields: dict) -> int:
    try:
        if testSetId := GetPTTestSetId.RetrieveTestSetWithVersion(featureFileName, releaseVersion):
            return testSetId
        else:
            return CreatePTTestSet.CreatePTTestSet(featureFileName, releaseVersion, customFields)

    except Exception as msg:
        print ("Something went wrong in CreateTestSetFromFeature(): ", msg)
        raise Exception (msg)

def PostToPractiTest(featureFileName, passFailStatus, testOutputMessage): 
    try:
        #get associated test id (in PT) based on 'feature name' from bdd
        testId = GetPTTest.RetrieveTestId(featureFileName)

        #get associated instance id for testId provided
        instanceId = GetPTInstance.RetrieveInstanceId(clonedTestSetId, testId)
        
        if not isinstance(passFailStatus, TestResultStatus):
            raise TypeError("passFailStatus must be an instance of enum TestResultStatus")

        #post test results
        postId = PostTestResults.PostTestResultsToPT(instanceId, passFailStatus, testOutputMessage)
        print ("Post id: ", postId)
        
    except Exception as msg:
        print ("Something went wrong in PostToPractiTest(): ", msg)
        raise Exception (msg)

def PostToPractiTestWithFile(instanceId: int, passFailStatus: bool, fileDir: str, fileName: str):
    try:
        return PostTestResults.PostTestResultsWithFile(instanceId, passFailStatus, fileDir, fileName)
    
    except Exception as msg:
        print ("Something went wrong in PostToPractiTestWithLogs(): ", msg)
        raise Exception (msg)

def RetrieveTestId(testName: str) -> int:
    try:
        return GetPTTest.RetrieveTestIdByName(testName)
    
    except Exception as msg:
        print ("Something went wrong in RetrieveTestId(): ", msg)
        raise Exception (msg)

def CreateInstance(testSetId: int, testId: int) -> int:
    try:
        return CreatePTInstance.CreatePTInstance(testSetId, testId)
    
    except Exception as msg:
        print ("Something went wrong in CreateInstance(): ", msg)
        raise Exception (msg)
