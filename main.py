import datetime

from delete_expired_files import delete_expired_files
from delete_empty_folders import delete_empty_folders
from backup_files import backup_files 

source = 'E:/Source_folder/'
destination = 'E:/Backup_folder/'
log = 'E:\Backup_folder\Logs'

# Usage
backup_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/", log, 7)
delete_empty_folders(destination,log)
delete_expired_files(log)