"""
Utility to split large CSV/Excel files into smaller chunks
"""

import pandas as pd
import os
from pathlib import Path

def split_file(file_path, chunk_size=50000, output_dir='data/split'):
    """
    Split a large file into smaller chunks
    
    Args:
        file_path: Path to the file to split
        chunk_size: Number of rows per chunk
        output_dir: Directory to save the chunks
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get file info
    file_name = Path(file_path).stem
    file_ext = Path(file_path).suffix
    
    # Read and split file
    if file_ext.lower() in ['.xlsx', '.xls', '.xlsb']:
        df_chunks = pd.read_excel(file_path, chunksize=chunk_size)
    else:
        df_chunks = pd.read_csv(file_path, chunksize=chunk_size)
    
    # Save chunks
    for i, chunk in enumerate(df_chunks):
        chunk_path = f"{output_dir}/{file_name}_part{i+1}{file_ext}"
        if file_ext.lower() in ['.xlsx', '.xls', '.xlsb']:
            chunk.to_excel(chunk_path, index=False)
        else:
            chunk.to_csv(chunk_path, index=False)
        print(f"Created {chunk_path}")