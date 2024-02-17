import json
import subprocess




def run_cmd(filename, solc) -> dict:
    try:
        result = subprocess.run(['myth', 'analyze', filename, '--solv', f'{solc}', '-o', 'json'], capture_output=True, text=True)
        resultInDict = json.loads(result.stdout)
        return resultInDict
    except subprocess.CalledProcessError as e:
        print(f"Error running slither: {e}")    
        return {}   
def checkIssues(resultInJson: dict[str, dict]) -> int:
    if (resultInJson['success']):
        detectors = resultInJson['issues']
        for detector in detectors:
            if (detector['swc-id'] == '101'):
                return 2
    return -1

def checkError(resultInJson: dict[str, dict]) :
    pass
def getMythrilResult(filename, solc):
    resultInJson = run_cmd(filename, solc)
    if (checkError(resultInJson)):
        return -1
    else:
        return checkIssues(resultInJson)