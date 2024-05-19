import os
import datetime

def delete_empty_folders(root,log_file):
    log =""
    deleted = set()
    
    for current_dir, subdirs, files in os.walk(root, topdown=False):

        still_has_subdirs = False
        for subdir in subdirs:
            if os.path.join(current_dir, subdir) not in deleted:
                still_has_subdirs = True
                break
    
        if not any(files) and not still_has_subdirs:
            os.rmdir(current_dir)
            deleted.add(current_dir)
            
    log = log + repr(deleted)+"\n"
    log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
    with open(log_file, "a", encoding="utf-8") as text_file:
        text_file.write(log)
    
    return deleted