import os
import difflib
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

def remove_cpp_comments(code):
    code_without_comments = []
    in_multiline_comment = False

    for line in code:
        line = re.sub(r'//.*', '', line)

        if in_multiline_comment:
            if '*/' in line:
                in_multiline_comment = False
            continue
        elif '/*' in line:
            in_multiline_comment = True
            if '*/' in line:
                in_multiline_comment = False
            line = line[:line.index('/*')]

        line = line.strip()
        if line and not line.startswith("int main() {") and not line.endswith("}")  and not re.match(r'^\s*{\s*}$', line) and not re.match(r'^return 0;', line) and not line.startswith("#include"):
            code_without_comments.append(line)

    return code_without_comments

def compare_cpp_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        code1 = f1.readlines()
        code2 = f2.readlines()

    code1_without_comments = remove_cpp_comments(code1)
    code2_without_comments = remove_cpp_comments(code2)

    similarity = difflib.SequenceMatcher(None, code1_without_comments, code2_without_comments).ratio()

    common_lines = set(code1_without_comments).intersection(code2_without_comments)
    
    return similarity, common_lines

async def compare_all_cpp_files_async(folder_path):
    files = os.listdir(folder_path)
    
    cpp_files = [file for file in files if file.endswith(".cpp")]
    
    if len(cpp_files) < 2:
        print("There are not enough C++ files in the folder for comparison.")
        return
    
    tasks = []
    with ThreadPoolExecutor(max_workers=4) as executor:  
        loop = asyncio.get_event_loop()
        for i in range(len(cpp_files)):
            for j in range(i + 1, len(cpp_files)):
                file_1_path = os.path.join(folder_path, cpp_files[i])
                file_2_path = os.path.join(folder_path, cpp_files[j])
                task = loop.run_in_executor(executor, compare_cpp_files, file_1_path, file_2_path)
                tasks.append((cpp_files[i], cpp_files[j], task))
    
    for file1_name, file2_name, task in tasks:
        similarity, common_lines = await task
        file1_name = os.path.splitext(file1_name)[0]  
        file2_name = os.path.splitext(file2_name)[0]  
        print(f"{file1_name}'s code's similarity to {file2_name}'s code is: {similarity * 100:.2f}%")
        print("Common Lines:")
        for line in common_lines:
            print(line)

if __name__ == "__main__":
    folder_path = "sample_codes"
    
    asyncio.run(compare_all_cpp_files_async(folder_path))
