from multiprocessing import Pool
import os
# import time
from script import extract_number, get_solc_version
from Slither import getSlitherResult
from Mythril import getMythrilResult
src_folder = os.path.join(os.getcwd(), 'Ethereum_smart_contract_datast', 'Ethereum_smart_contract_datast', 'contract_dataset_ethereum')
result_file = os.path.join(os.getcwd(), 'IOU', 'resultTest.txt')
result_remote_file = os.path.join(os.getcwd(), 'IOU', 'resultTestFromRemote.txt')
merge_file = os.path.join(os.getcwd(), 'IOU', 'resultMerge.txt')
folders = []
files = []
files_excluded = []
num_process = os.cpu_count() 
if (num_process != None):
    num_process = num_process - 6
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
    files_excluded.extend(files_sorted[3000:3100])

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
    with open(merge_file, "r") as file:
        lines = file.readlines()

    # Sort the lines based on the numeric part of the file names
    sorted_lines = sorted(lines, key=lambda x: extract_number(x.split(',')[0]))

    # Write the sorted lines back to the result file
    with open(merge_file, "w") as file:
        file.writelines(sorted_lines)

def merge_files(file1, file2):
    # Read the contents of the first file
    with open(file1, 'r') as f:
        lines1 = f.readlines()

    # Read the contents of the second file
    with open(file2, 'r') as f:
        lines2 = f.readlines()

    # Store filenames and numbers in a dictionary
    data = {}
    for line in lines1 + lines2:
        filename, number = line.strip().split(', ')
        number = int(number)
        if number != -1:
            if filename in data:
                data[filename] = max(number, data[filename])
            else:
                data[filename] = number

    # Write merged data to a new file
    with open(merge_file, 'w') as f:
        for filename, number in sorted(data.items()):
            f.write(f"{filename}, {number}\n")

if __name__ == "__main__":
    # runToolConcurrently()
    orderResult()
    # merge_files(result_file, result_remote_file)

    



    # endtime = time.time()
    # print(f"Time taken {endtime-starttime} seconds")