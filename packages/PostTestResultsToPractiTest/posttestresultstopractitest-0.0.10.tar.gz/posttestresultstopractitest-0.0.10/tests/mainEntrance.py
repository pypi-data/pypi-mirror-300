from PostTestResultsToPractiTest import Orchestrator
from PostTestResultsToPractiTest.EnumClass import TestResultStatus

def main():
    # Clone test set with instances and post results.
    Orchestrator.CreateTestSetProcess()
    Orchestrator.PostToPractiTest("AKCanBumpOpenOrders.feature", TestResultStatus.PASS, "Output message if any")

    # Create test set, fill with instances, and post results
    customFields = {'---f-112372': 'Example'}
    testSetId = Orchestrator.CreateTestSetFromFeature(featureFileName="AKCanBumpOpenOrders.feature", releaseVersion="1.0.0", customFields=customFields)
    # The next three lines should be repeated for the amount of tests there are in the test set.
    testId = Orchestrator.RetrieveTestId("Example test name.")
    instanceId = Orchestrator.CreateInstance(testSetId, testId)
    Orchestrator.PostToPractiTestWithFile(instanceId, passFailStatus=True, fileDir="C:/ExampleDir", fileName="ExampleFile.log")
    
main()