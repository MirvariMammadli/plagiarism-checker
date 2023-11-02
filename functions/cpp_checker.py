import difflib
from functions.remover import remover

def cpp_checker(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        code1 = f1.readlines()
        code2 = f2.readlines()

    code1_without_comments = remover(code1)
    code2_without_comments = remover(code2)

    similarity = difflib.SequenceMatcher(None, code1_without_comments, code2_without_comments).ratio()

    common_lines = set(code1_without_comments).intersection(code2_without_comments)
    
    return similarity, common_lines
