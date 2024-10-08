import json
from PostTestResultsToPractiTest import PT_APIRequest
from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTProjectId
from PostTestResultsToPractiTest import Constants

def CreatePTTestSet(featureFileName: str, releaseVersion: str = None, customFields: dict = None) -> int:
    """Create a PractiTest test set provided a feature file name.

    :param featureFileName: Name of feature file.
    :param releaseVersion: Release version for test set run.
    :param customFields: Dict of any desired custom fields for test set.
    :return: PractiTest id for created test set.
    """
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    testSetDict = {"data":{"type":"sets","attributes":{"name":featureFileName, "version": releaseVersion}}}
    testSetDict["data"]["attributes"]["custom-fields"] = customFields
    jsonData = json.dumps(testSetDict)
    
    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId +"/sets.json", "post", jsonData)

    if res.status_code == 200:
        responseData = json.loads(res.content)

        data = responseData['data']
   
        newTestSetId = data['id']
        return newTestSetId
    else:
        raise Exception ("Call to create test set was unsuccessful with status code", res.status_code)