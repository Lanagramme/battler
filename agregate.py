import os
import json

def read_files_in_folder(folder_path):
    file_data = {}
    valid_extensions = {".py", ".txt", ".md"}  # add more as needed
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip files that don't match our valid extensions
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in valid_extensions:
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data[file_path] = f.read()
            except UnicodeDecodeError:
                # If the file isn't actually UTF-8 encoded
                print(f"Skipping file (not valid UTF-8): {file_path}")

    return file_data

if __name__ == "__main__":
    folder_path = "./"
    output_file = "output.json"
    
    files_content = read_files_in_folder(folder_path)
    
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(files_content, out, ensure_ascii=False, indent=2)
    
    print(f"File contents have been written to {output_file}")
