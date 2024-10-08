import json
import os
import base64
from PostTestResultsToPractiTest import PT_APIRequest
from PostTestResultsToPractiTest import GetConfigValues
from PostTestResultsToPractiTest import GetPTProjectId
from PostTestResultsToPractiTest import Constants
from PostTestResultsToPractiTest.EnumClass import TestResultStatus

def PostTestResultsToPT(instanceId, passFailStatus, testOutputMessage):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
  
    print ("passfailStatus..", passFailStatus)  
    if passFailStatus.value == "pass":
        exit_code = 0
    else:
        exit_code = 1
        
    jsonData = json.dumps({"data":{"type":"instances","attributes":{"instance-id":instanceId,"exit-code":exit_code,"automated-execution-output":testOutputMessage}}})
    
    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/runs.json", "post", jsonData)
    
    if res.status_code == 200:
        responseData = json.loads(res.content)
        data = responseData['data']
        postId = data['id']
        return postId
    else:
        raise Exception ("Call to post-results-to-PT was unsuccessful with status code", res.status_code)

def PostTestResultsWithFile(instanceId: int, passFailStatus: bool, fileDir: str, fileName: str) -> int:
    """Post test results to PractiTest along with logs.

    :param instanceId: Instance id to attach results to.
    :param passFailStatus: Whether the test passed or failed.
    :param fileDir: Directory where file is stored.
    :param fileName: Name of file.
    :return: PractiTest result id.
    """
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()

    exitCode = 0 if passFailStatus else 1

    file = open(os.path.join(fileDir, fileName), "rb")

    jsonData = json.dumps({'data': {
                                'type': 'instances',
                                'attributes': {
                                    'instance-id': instanceId,
                                    'exit-code': exitCode
                                },
                                'files': {
                                    'data':[{
                                        'content_encoded': base64.b64encode(file.read()).decode('utf-8'),
                                        'filename': fileName
                                }]
                                }
                            }})

    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/runs.json", "post", jsonData)

    if res.status_code == 200:
        responseData = json.loads(res.content)
        data = responseData['data']
        postId = data['id']
        return postId
    else:
        raise Exception ("Call to post-results-to-PT was unsuccessful with status code", res.status_code)