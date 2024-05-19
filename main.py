import datetime

from delete_expired_files import delete_expired_files
from delete_empty_folders import delete_empty_folders
from backup_files import backup_files 
from backup_containers import backup_containers

source_directories = ['D:/Source_folder/',"E:/123_Projekty/"]
dest_dir = 'D:/Backup_folder/'
log_dir = 'D:\Backup_folder\Logs'

if __name__ == "__main__":
    # Usage
    log_file = log_dir+"\\log_"+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".txt"
    dest_backup_folder_name = dest_dir+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/"

    for src_dir in source_directories:
        backup_files(src_dir, dest_backup_folder_name, log_file, 7)
    delete_empty_folders(dest_dir,log_file)
    delete_expired_files(log_file)
    backup_containers(dest_dir,log_file)