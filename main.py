import datetime

from delete_expired_files import delete_expired_files
from delete_empty_folders import delete_empty_folders
from backup_files import backup_files 
from backup_containers import backup_containers

source = 'D:/Source_folder/'
destination = 'D:/Backup_folder/'
log = 'D:\Backup_folder\Logs'

if __name__ == "__main__":
    # Usage
    backup_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/", log, 7)
    delete_empty_folders(destination,log)
    delete_expired_files(log)
    backup_containers(destination,log)