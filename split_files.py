"""
Script to split large data files
"""

from data_splitter import split_file
import os
from config import DATA_DIR, DATA_FILES

def main():
    # List of large files to split
    large_files = ['clears.csv', 'plays.csv']
    
    for file in large_files:
        file_path = os.path.join(DATA_DIR, file)
        if os.path.exists(file_path):
            print(f"Splitting {file}...")
            split_file(file_path)
            print(f"Finished splitting {file}")

if __name__ == "__main__":
    main()