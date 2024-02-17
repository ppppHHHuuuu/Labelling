import json
import subprocess

issues = ['timestamp']

def run_cmd(filename, solc) -> dict:
    try:
        result = subprocess.run(['slither', filename, '--solc-solcs-select', f'{solc}', '--json', '-'], capture_output=True, text=True)
        resultInDict = json.loads(result.stdout)
        return resultInDict
    except subprocess.CalledProcessError as e:
        print(f"Error running slither: {e}")    
        return {}
    
def checkIssues(resultInJson: dict[str, dict]) -> int:
    if (resultInJson == {}): return 0
    if (resultInJson['success']):
        detectors = resultInJson['results']['detectors']
        for detector in detectors:
            if (detector['check'] in issues):
                return 1
    return 0

def checkError(resultInJson: dict):
    pass
def getSlitherResult(filename, solc):
    resultInJson = run_cmd(filename, solc)
    if (checkError(resultInJson)):
        return -1
    else:
        return checkIssues(resultInJson)
    