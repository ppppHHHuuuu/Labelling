from multiprocessing import Pool
import os
# import time
from script import extract_number, get_solc_version
from Slither import getSlitherResult
from Mythril import getMythrilResult
src_folder = os.path.join(os.getcwd(), 'Ethereum_smart_contract_datast', 'Ethereum_smart_contract_datast', 'contract_dataset_ethereum')
result_file = os.path.join(os.getcwd(), 'IOU', 'resultTest.txt')

folders = []
files = []
files_excluded = []
num_process = os.cpu_count() - 6
if (num_process != None):
    num_process = num_process
# unique_lines = set()
# with open(result_file, 'r') as result:
#     for line in result.split(',')[0]:
#         unique_lines.add(line)  
def getFilesNeeded() :
    global files_excluded
    for folder_name in os.listdir(src_folder):  
        for filename in os.listdir(os.path.join(src_folder, folder_name)):
            if (filename == '.DS_Store'):
                continue
            files.append(os.path.join(src_folder, folder_name, filename))

    files_sorted = sorted(files, key=lambda x: extract_number(os.path.basename(x)))
    # print ("files_sorted, ", files_sorted)    
    files_excluded.extend(files_sorted[2000:2100])

def process_file(file_path):
    file_name = os.path.basename(file_path)
    solc = get_solc_version(file_path)  # Implement this function to get Solc version
    mythril_result = getMythrilResult(file_path, solc)
    result_line = f'{file_name}, {mythril_result}\n'
    print (result_line)
    # if result_line not in unique_lines:
    with open(result_file, 'a+') as result:
        result.write(result_line)


def runToolConcurrently():

    getFilesNeeded()
    with Pool(processes = num_process) as pool:
        results = pool.map(process_file, files_excluded)

def orderResult():           
    # Read the lines from the result file
    with open(result_file, "r") as file:
        lines = file.readlines()

    # Sort the lines based on the numeric part of the file names
    sorted_lines = sorted(lines, key=lambda x: extract_number(x.split(',')[0]))

    # Write the sorted lines back to the result file
    with open(result_file, "w") as file:
        file.writelines(sorted_lines)


if __name__ == "__main__":
    runToolConcurrently()
    # orderResult()
    



    # endtime = time.time()
    # print(f"Time taken {endtime-starttime} seconds")