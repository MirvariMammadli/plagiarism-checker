import os
import asyncio
import pandas as pd

from concurrent.futures import ThreadPoolExecutor
from functions.cpp_checker import cpp_checker

async def comparer(folder_path):
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

                if cpp_files[i][:4] == cpp_files[j][:4]:
                    continue

                task = loop.run_in_executor(executor, cpp_checker, file_1_path, file_2_path)
                tasks.append((cpp_files[i], cpp_files[j], task))
    
    results = []
    for file1_name, file2_name, task in tasks:
        similarity, common_lines = await task
        file1_name = os.path.splitext(file1_name)[0]  
        file2_name = os.path.splitext(file2_name)[0]  
        # if similarity * 100:
        results.append((file1_name, file2_name, similarity * 100))

    file_name = folder_path.split('/')[2] + ' ' + folder_path.split('/')[3]

    df = pd.DataFrame(results, columns=['file1_name', 'file2_name', 'similarity'])
    df.to_excel(f'data/excels/{file_name}.xlsx', index=False)
    print("Results saved to comparison_results.xlsx")

