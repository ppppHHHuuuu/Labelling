import json
import subprocess

import time

timeout = 1000
def run_cmd(filename, solc) -> dict:

    try:
        start_time = time.time()

        result = subprocess.run(['myth', 'analyze', filename, '--solv', f'{solc}', '-o', 'json'], capture_output=True, 
                                text=True, timeout=timeout)
        end_time = time.time()
        time_difference = end_time - start_time

        print("Time difference:", time_difference, "seconds")
        
        if result.returncode != 0:
            print(f"Error running command: {result.stderr}")
            return {'timeout': 0}

        resultInDict = json.loads(result.stdout)
        resultInDict['timeout'] = -1

        return resultInDict
    except subprocess.TimeoutExpired:
        print("Error: Process timed out")
        return {'timeout': 4}  # Return timeout metric in milliseconds
    except subprocess.CalledProcessError as e:
        print(f"Error running slither: {e}")
        return {'timeout': 0}  # Return 0 timeout if there's an error
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
    try:
        if (resultInJson['timeout'] == timeout):
            return -1 
        if (resultInJson['timeout'] == 0):
            return -1
        else:
            print('goes to checkIssues')
            return checkIssues(resultInJson)
    except:
        return -1
