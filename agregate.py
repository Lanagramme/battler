import os
import json

def read_files_in_folder(folder_path):
    file_data = {}
    valid_extensions = {".py", ".txt", ".md"}  # add more as needed
    
    for root, _, files in os.walk(folder_path):
        # Skip unwanted directories
        if "env" in root.split(os.sep) or ".git" in root.split(os.sep):
            continue
        
        for file in files:
            # Skip .git* files
            if file.startswith(".git"):
                continue
            
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file_path)
            
            # Skip files that don't match our valid extensions
            if ext.lower() not in valid_extensions:
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data[file_path] = f.read()
            except UnicodeDecodeError:
                print(f"Skipping file (not valid UTF-8): {file_path}")
    
    return file_data

if __name__ == "__main__":
    folder_path = "./"
    output_file = "output.json"
    
    # Remove output.json if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    files_content = read_files_in_folder(folder_path)
    
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(files_content, out, ensure_ascii=False, indent=2)
    
    print(f"File contents have been written to {output_file}")
