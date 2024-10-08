import json
from PostTestResultsToPractiTest import PT_APIRequest
from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTProjectId
from PostTestResultsToPractiTest import Constants

def RetrieveTestId(filterByAutomationName):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/tests.json")
    
    if res.status_code == 200:
        allTests = json.loads(res.content)
        allTestsData = allTests['data']

        myTestData = list(filter(lambda myData: myData.get('attributes').get('custom-fields').get('---f-114228') == filterByAutomationName, allTestsData ))
       
        if len(myTestData) != 0:
            myTestId = myTestData[0]['id']
            print ("Test id:", myTestId)
            return myTestId
        else:
            raise Exception ("No associated test is found in PT that has the key of 'Automation Name = '" + filterByAutomationName)
    else:
        raise Exception ("Call to get a list of tests is unsuccessful with status code", res.status_code)

def RetrieveTestIdByName(testName: str) -> int:
    """Retrieve PractiTest test id provided the test name.

    :param testName: Name of test.
    :return: PractiTest test id.
    """
    projectId = GetPTProjectId.RetrieveProjectId()
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/tests.json?name_exact=" + testName)

    if res.status_code == 200:
        allTests = json.loads(res.content)
        testsData = allTests["data"]
        desiredTestData = list(filter(lambda desiredData:desiredData['attributes']['name']==testName, testsData))

        if len(desiredTestData) != 0:
            testId = desiredTestData[0]['id']
            return testId
        else:
            raise Exception ("No associated test is found in PT that has the key of 'Test Name = '" + testName)
    else:
        raise Exception ("Call to get a list of tests is unsuccessful with status code", res.status_code)
