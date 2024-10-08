import json
from PostTestResultsToPractiTest import PT_APIRequest
from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTProjectId
from PostTestResultsToPractiTest import Constants
from PostTestResultsToPractiTest import GetPTInstance

def CreatePTInstance(testSetId: int, testId: int) -> int:
    """Create PractiTest instance given a test set id and test id.

    :param testSetId: PractiTest id for target test set.
    :param testId: PractiTest id for test to create instance from.
    :return: PractiTest id for created instance.
    """
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()

    if instanceId := GetPTInstance.RetrieveInstanceId(testSetId, testId):
        return instanceId
    
    jsonData = json.dumps({"data":{"type":"instances","attributes":{"test-id":testId, "set-id": testSetId}}})
    
    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId +"/instances.json", "post", jsonData)

    if res.status_code == 200:
        responseData = json.loads(res.content)

        data = responseData['data']
   
        newInstanceId = data['id']
        return newInstanceId
    else:
        raise Exception ("Call to create instance was unsuccessful with status code", res.status_code)
