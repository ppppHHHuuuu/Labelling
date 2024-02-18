import os

src_file = os.path.join(os.getcwd(), 'result_send_1.txt')
dest_file = os.path.join(os.getcwd(), 'result_test.txt')

# Read the file and split lines
with open(src_file, "r") as file:
    lines = file.readlines()

# Initialize a dictionary to store file names and their counts
file_counts = {}

# Iterate through the lines and count file occurrences
for line in lines:
    file_name, _ = line.strip().split(", ")  # Extract file name from each line
    if file_name in file_counts:
        file_counts[file_name] += 1
    else:
        file_counts[file_name] = 1

# Initialize a list to store lines with unique file names
unique_lines = []

# Iterate through the lines again and keep only the first occurrence of each file name
for line in lines:
    file_name, _ = line.strip().split(", ")  # Extract file name from each line
    if file_counts[file_name] == 1:
        unique_lines.append(line)
    else:
        print(f"dup file: {file_name}, {file_counts[file_name]}")
        file_counts[file_name] -= 1  # Decrement count for duplicate file names

# Write the unique lines back to the file
with open(dest_file, "w") as file:
    file.writelines(unique_lines)

print("Duplicates removed and unique file list written to file_list_unique.txt")
