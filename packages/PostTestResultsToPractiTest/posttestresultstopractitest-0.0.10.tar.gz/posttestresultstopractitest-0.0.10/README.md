# PostTestResultsToPractiTest package

## Config file requirements: 
    Need to create a file called userInputs.ini at the root of your project and add the following lines to the content of that file.  You'll need to update those values with your specific ones. 
    
        ```
        [UserInputs]
        PractiTestProjectName=<PractiTest's Project Name>
        PractiTestTestSetName_ToCloneFrom=<TestSetNameToCloneFrom>
        PractiTestTestSetName_New=<NewTestSetNameToBeCreated>
        PT_Token=<yourPractiTestToken>
        ```


## This package makes use of PractiTest's APIs to do the following:

### 1. Use this package to clone test_set (test set needs to be created along with its instances before usage)

    Example of how to use it (in Python):
    ```
        from PostTestResultsToPractiTest import Orchestrator
        Orchestrator.CreateTestSetProcess()
    ```

### 2. Use this package to post test results to the test_set created in step1.

    Example of how to use it (in Python):
    ```
        from PostTestResultsToPractiTest import Orchestrator
        from PostTestResultsToPractiTest.EnumClass import TestResultStatus
        Orchestrator.PostToPractiTest("NameOfYourFeatureFileInBDD-including-extension-.feature", TestResultStatus.UNSTABLE, "Output message if any")
    ```
    Note that TestResultStatus is an enum class, available values are TestResultStatus.PASS, estResultStatus.FAIL, and TestResultStatus.UNSTABLE

### 3. Use this package to create test set, fill with instances, and post results all within an automation run.

    Example of how to use it (in Python):
    ```
        from PostTestResultsToPractiTest import Orchestrator
        customFields = {'---f-112372': 'Example'}
        testSetId = Orchestrator.CreateTestSetFromFeature(featureFileName, releaseVersion, customFields)
        testId = Orchestrator.RetrieveTestId(testName)
        instanceId = Orchestrator.CreateInstance(testSetId, testId)
        Orchestrator.PostToPractiTestWithFile(instanceId, passFailStatus, fileDir, fileName)
    ```
    Note that passFailStatus is just a boolean value on whether the test passed or failed.
    The variables fileDir and fileName are the directory and file name respectively for the file that you would like to attach
    with your test results (logs, reports, etc.).