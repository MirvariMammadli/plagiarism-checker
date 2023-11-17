import os
import shutil

def extract_submission_number(submission_str):
    try:
        return int(submission_str[3:4])
    except ValueError:
        return 0  

def group_and_sort_files(input_directory, output_directory):
    files = os.listdir(input_directory)

    grouped_files = {}

    for file_name in files:
        parts = file_name.split('_')

        problem_name = parts[1]
        submission_number = extract_submission_number(parts[-1])

        if problem_name not in grouped_files:
            grouped_files[problem_name] = []

        grouped_files[problem_name].append((file_name, submission_number))

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for problem_name, file_info_list in grouped_files.items():
        file_info_list.sort(key=lambda x: x[1])

        problem_folder_path = os.path.join(output_directory, problem_name)
        if not os.path.exists(problem_folder_path):
            os.makedirs(problem_folder_path)

        for file_info in file_info_list:
            _, submission_number = file_info
            submission_folder_path = os.path.join(problem_folder_path, f'submission_{submission_number}')
            if not os.path.exists(submission_folder_path):
                os.makedirs(submission_folder_path)

            file_name, _ = file_info
            original_file_path = os.path.join(input_directory, file_name)
            new_file_path = os.path.join(submission_folder_path, file_name)
            shutil.copy(original_file_path, new_file_path)

def rename_files(input_directory):
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            parts = file_name.split('_')

            problem_name = parts[1]
            submission_number = extract_submission_number(parts[-1])
            country_code = parts[-1].split('-')[0]

            new_file_name = f"{country_code}.{submission_number}.{parts[0]}.{parts[-1].split('.')[-1]}"

            old_file_path = os.path.join(root, file_name)
            new_file_path = os.path.join(root, new_file_name)
            os.rename(old_file_path, new_file_path)

if __name__ == "__main__":
    input_directory = "data/ioi2020_day1"
    output_directory = "data/ioi2020_day1_sorted"

    group_and_sort_files(input_directory, output_directory)

    rename_files(output_directory)
