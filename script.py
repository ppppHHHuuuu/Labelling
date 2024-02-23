import json
import os
import re
import subprocess
from Mythril import getMythrilResult
from Slither import getSlitherResult
src_folder = os.path.join(os.getcwd(), 'Ethereum_smart_contract_datast', 'Ethereum_smart_contract_datast', 'contract_dataset_ethereum')

result_file = os.path.join(os.getcwd(),'IOU', 'result.txt')

valid_solcs: list[str] = ['0.8.21', '0.8.20', '0.8.19', '0.8.18', '0.8.17', '0.8.16', '0.8.15', '0.8.14', '0.8.13', '0.8.12', '0.8.11', '0.8.10', '0.8.9', '0.8.8', '0.8.7', '0.8.6', '0.8.5', '0.8.4', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.6', '0.7.5', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.7.0', '0.6.12', '0.6.11', '0.6.10', '0.6.9', '0.6.8', '0.6.7', '0.6.6', '0.6.5', '0.6.4', '0.6.3', '0.6.2', '0.6.1', '0.6.0', '0.5.17', '0.5.16', '0.5.15', '0.5.14', '0.5.13', '0.5.12', '0.5.11', '0.5.10', '0.5.9', '0.5.8', '0.5.7', '0.5.6', '0.5.5', '0.5.4', '0.5.3', '0.5.2', '0.5.1', '0.5.0', '0.4.26', '0.4.25', '0.4.24', '0.4.23', '0.4.22', '0.4.21', '0.4.20', '0.4.19', '0.4.18', '0.4.17', '0.4.16', '0.4.15', '0.4.14', '0.4.13', '0.4.12', '0.4.11', '0.4.10', '0.4.9', '0.4.8', '0.4.7', '0.4.6', '0.4.5', '0.4.3', '0.4.2', '0.4.1', '0.4.0']
valid_solcs_str = ",".join(valid_solcs)
def extract_number(filename):
    digits = ''.join(filter(str.isdigit, filename))
    return int(digits) if digits else -1  # Return -1 if no digits found
def get_solc_version(
        file_name: str
    ) -> str:
        """Xác định phiên bản solidity được khai báo trong mã nguồn

        Args:
            sub_container_file_path (str): _description_
            file_name (str): _description_

        Returns:
            str | int: -1 Nếu không thể xác định được phiên bản
                        0 Nếu phiên bản xác định được không được hỗ trợ
        """
        file_path = os.path.join(src_folder, file_name)
        solc: str = ""
        with open(file_path, "r") as file:
            source_code: str = file.read()

            # Loại bỏ khối comment
            source_code = re.sub(r"/\*.*?\*/", "", source_code, flags=re.DOTALL)
            lines: list[str] = source_code.splitlines()
            for line in lines:
                line: str = line.split(r"//")[0]
                match: re.Match[str] | None = re.search(r"pragma\s+solidity\s+([<>=^]*[\d]+\.[\d]+(\.[\d]+)?)", line)
                if match:
                    solc = match.group(1)
                    if (solc.count('.') == 1):
                        solc += '.0'
                    break
            if (solc == ""):
                return "No solc given"
            res: str = ""
            match solc[0]:
                case '^':
                    res = solc[1:]
                    if (res not in valid_solcs):
                        return "Not supported solc"
                case '>':
                    if (solc[1] == '='):
                        res = solc[2:]
                    else:
                        try:
                            i: int = valid_solcs.index(solc[1:])
                            if (i == 0):
                                return "Not supported solc"
                            res = valid_solcs[i-1]
                        except ValueError:
                            return "Not supported solc"
                case '<':
                    if (solc[1] == '='):
                        res = solc[2:]
                    else:
                        try:
                            i: int = valid_solcs.index(solc[1:])
                            if (i == len(valid_solcs) - 1):
                                return "Not supported solc"
                            res = valid_solcs[i+1]
                        except ValueError:
                            return "Not supported solc"
                case _:
                    return solc if solc in valid_solcs else "Not supported solc"

            return res if res[0].isdigit() else "Not supported solc"
def main():
    unique_lines = set()
    files = []
    with open(result_file, 'r') as result:
        for line in result:
            unique_lines.add(line)  
    print (unique_lines)
    for folder_name in os.listdir(src_folder):  
        for filename in os.listdir(os.path.join(src_folder, folder_name)):
            if (filename == '.DS_Store'):
                continue
            files.append(os.path.join(src_folder, folder_name, filename))
    count = 100
    for file_path in sorted(files, key=lambda x: extract_number(os.path.basename(x))):
        # print (file_path)
        # count -= 1
        # if (count < 0):
        #     break
        with open (file_path) as f:
            file_name = os.path.basename(f.name)
            solc = get_solc_version(f.name)
            print(f.name)
            slither_result = getSlitherResult(filename=f.name, solc =solc) 
            with open (result_file, 'a+') as result: 
                result_line = f'{file_name}, {slither_result}\n'
                # print(result_line)
                if (result_line not in unique_lines):
                    result.write(result_line)
                    unique_lines.add(result_line)
if __name__=="__main__":
    main()
    


