import os
import asyncio
from functions.comparer import comparer

def process_all_problems(sorted_folder_path):
    problems = os.listdir(sorted_folder_path)

    for problem in problems:
        problem_path = os.path.join(sorted_folder_path, problem)
        submission_numbers = os.listdir(problem_path)
        
        for submission_number in submission_numbers:
            submission_path = os.path.join(problem_path, submission_number)
            
            asyncio.run(comparer(submission_path))

    # asyncio.run(comparer(sorted_folder_path))

if __name__ == "__main__":
    sorted_folder_path = "data/ioi2020_day1_sorted"
    # sorted_folder_path = "sample_codes"

    process_all_problems(sorted_folder_path)
