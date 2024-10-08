import json
from PostTestResultsToPractiTest import PT_APIRequest
from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTProjectId
from PostTestResultsToPractiTest import Constants

def RetrieveInstanceId(filterByTestSetId, filterByTestId):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL+ "/projects/" + projectId + "/instances.json?set-ids=" + filterByTestSetId)

    if res.status_code == 200:
        allInstances = json.loads(res.content)
        allInstancesData = allInstances['data']
        myInstanceData = list(filter(lambda myData:myData['attributes']['test-id']==int(filterByTestId), allInstancesData))   
        #print ("testData:", myInstanceData)
               
        if len(myInstanceData) != 0:
            myInstanceId = myInstanceData[0]['id']
            return myInstanceId
        else:
            return None
    else:
        raise Exception ("Call to get a list of instances is unsuccessful with status code", res.status_code)
