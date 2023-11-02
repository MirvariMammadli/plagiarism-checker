import asyncio

from functions.comparator import comparer

if __name__ == "__main__":
    folder_path = "sample_codes"
    
    asyncio.run(comparer(folder_path))
