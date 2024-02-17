from multiprocessing import Pool
import os
import time

files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
def printFiles(file):
    print(f"start process: {file}")
    print(f"processing process: {file}")
    time.sleep(1)
    print(f"end process: {file}")

num_process = os.cpu_count()

if __name__ == "__main__":
    starttime = time.time()
    with Pool(processes = num_process) as pool:
        pool.map(printFiles, files)
    endtime = time.time()
    print(f"Time taken {endtime-starttime} seconds")