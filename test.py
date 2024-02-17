from multiprocessing import Pool
import os
import time
from script import extract_number, get_solc_version
from Slither import getSlitherResult
src_folder = os.path.join(os.getcwd(), 'Ethereum_smart_contract_datast', 'Ethereum_smart_contract_datast', 'contract_dataset_ethereum')
result_file = os.path.join(os.getcwd(), 'resultTest2.txt')

folders = []
files = []
files_excluded = []
num_process = os.cpu_count()
if (num_process != None):
    num_process = num_process - 2

def getFilesNeeded() :
    global files_excluded
    for folder_name in os.listdir(src_folder):  
        for filename in os.listdir(os.path.join(src_folder, folder_name)):
            if (filename == '.DS_Store'):
                continue
            files.append(os.path.join(src_folder, folder_name, filename))
    files_sorted = sorted(files, key=lambda x: extract_number(os.path.basename(x)))
    files_excluded.extend(files_sorted[10001:40000])

def process_file(file_path):
    file_name = os.path.basename(file_path)
    solc = get_solc_version(file_path)  # Implement this function to get Solc version
    slither_result = getSlitherResult(file_path, solc)
    result_line = f'{file_name}, {slither_result}\n'
    with open(result_file, 'a+') as result:
        result.write(result_line)


def runToolConcurrently():
    # unique_lines = set()
    # with open(result_file, 'r') as result:
    #     for line in result:
    #         unique_lines.add(line)  
    # print(unique_lines)
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
    # runToolConcurrently()
    orderResult()
    



    # endtime = time.time()
    # print(f"Time taken {endtime-starttime} seconds")