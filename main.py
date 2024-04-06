import shutil
import os
import datetime

import sys
from hashlib import sha256

sha = sha256()

def hash_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        
    sha.update(data)
    shaHashed = sha.hexdigest()
    
    return(shaHashed)

def copy_files(src_dir, dest_dir):
    # Check if both the source and destination directories exist
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir+"/")

    # List all files in the source directory
    files = os.listdir(src_dir)
    print(files)

    for file in files:
        #print(src_dir+file)
        
        if(os.path.isdir(src_dir+file)):
            print(f"Recursing directory: {file}")
            if not os.path.exists(dest_dir+file+"/"):
                os.makedirs(dest_dir+file+"/")
            copy_files(src_dir+file+"/", dest_dir+file+"/")
            
        else:
            print(f"File: {file}")
            print(hash_file(src_dir+file))
            
            # Construct full file path
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            

            # Copy the file to the destination directory
            shutil.copy(src_file, dest_file)

source = 'C:/Users/mateu/OneDrive/SBS_SimpleBackupSolution/TESTGROUND/'
destination = 'C:/Users/mateu/OneDrive/SBS_SimpleBackupSolution/Backup_folder/'

# Usage
copy_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/")
