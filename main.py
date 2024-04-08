import shutil
import os
import datetime

import sys
from hashlib import sha256

sha = sha256()
log = ''

def hash_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        
    sha.update(data)
    shaHashed = sha.hexdigest()
    
    return(shaHashed)

def copy_files(src_dir, dest_dir):
    global log
    # Check if both the source and destination directories exist
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        log=log+f"Source directory {src_dir} does not exist.\n"
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
            log=log+f"Recursing directory: {file}\n"
            if not os.path.exists(dest_dir+file+"/"):
                os.makedirs(dest_dir+file+"/")
            copy_files(src_dir+file+"/", dest_dir+file+"/")
            
        else:
            print(f"File: {file}")
            log=log+f"File: {file}\n"
            print(hash_file(src_dir+file))
            log=log+f"{hash_file(src_dir+file)}\n"
            
            # Construct full file path
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            

            # Copy the file to the destination directory
            shutil.copy(src_file, dest_file)
            
    log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
    with open(destination+"\log_"+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".txt", "w") as text_file:
        text_file.write(log)
    

source = 'C:/Users/mateu/OneDrive/SBS_SimpleBackupSolution/Source_folder/'
destination = 'C:/Users/mateu/OneDrive/SBS_SimpleBackupSolution/Backup_folder/'

# Usage
copy_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/")
