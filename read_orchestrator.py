import subprocess
import os
import sys
from glob import glob

def process_pdf_folder(folder_path):
    # Create a pattern to match PDF files
    pdf_pattern = os.path.join(folder_path, '*.pdf')
    
    # List all PDF files in the specified folder
    pdf_files = glob(pdf_pattern)

    # Loop through all found PDF files and call read_invoice.py for each
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        subprocess.run(['python', 'read_invoice.py', pdf_file])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python read_orchestrate.py <path_to_pdf_folder>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_pdf_folder(folder_path)
