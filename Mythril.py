import json
import subprocess

import time


def run_cmd(filename, solc) -> dict:

    try:
        start_time = time.time()

        result = subprocess.run(['myth', 'analyze', filename, '--solv', f'{solc}', '-o', 'json'], capture_output=True, text=True)
        end_time = time.time()
        time_difference = end_time - start_time

        print("Time difference:", time_difference, "seconds")
        resultInDict = json.loads(result.stdout)
        return resultInDict
    except subprocess.CalledProcessError as e:
        print(f"Error running slither: {e}")    
        return {}   
def checkIssues(resultInJson: dict[str, dict]) -> int:
    if (resultInJson['success']):
        detectors = resultInJson['issues']
        for detector in detectors:
            print (detector['swc-id'])
            if (detector['swc-id'] == '101'):
                return 2
        print ('------')
    return 0

def checkError(resultInJson: dict[str, dict]) :
    pass
def getMythrilResult(filename, solc):
    resultInJson = run_cmd(filename, solc)
    if (checkError(resultInJson)):
        return -1
    else:
        return checkIssues(resultInJson)