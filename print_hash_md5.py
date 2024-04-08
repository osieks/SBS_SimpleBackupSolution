import shutil
import os
import datetime
import psycopg2
from hashlib import sha256

# secret data from local file
import secret

log = ''

def hash_file(filename):
    sha = sha256()
    with open(filename, 'rb') as f:
        data = f.read()
        
    sha.update(data)
    shaHashed = sha.hexdigest()
    
    return(shaHashed)

def copy_files(src_dir):
    global log
    # Check if both the source and destination directories exist
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return
    
    # List all files in the source directory
    files = os.listdir(src_dir)
    print(files)

    for file in files:
        #print(src_dir+file)
        
        if(os.path.isdir(src_dir+file)):
            print(f"Recursing directory: {file}")
            copy_files(src_dir+file+"/")
            
        else:
            print(f"File: {file}")
            file_hash = hash_file(src_dir+file)
            print("### "+file_hash)

    
source = 'E:/Source_folder/'

# Usage
copy_files(source)
