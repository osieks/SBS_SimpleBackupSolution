# Backup and Cleanup Script

This application is for defining data backups, retention, schedule (not yet implemented), etc.

This project contains Python scripts for backing up files, deleting expired files, removing empty folders, and backing up containers.

## Scripts

1. `backup_files.py`: This script backs up files from a source directory to a destination directory. It also logs the backup process.

2. `delete_expired_files.py`: This script deletes files that have passed their retention period.

3. `delete_empty_folders.py`: This script removes any empty folders in a given directory.

4. `backup_containers.py`: This script backs up containers.

## Usage

Change source, destination, and log paths.

```python
import datetime

from delete_expired_files import delete_expired_files
from delete_empty_folders import delete_empty_folders
from backup_files import backup_files 
from backup_containers import backup_containers

source = 'D:/Source_folder/'
destination = 'D:/Backup_folder/'
log = 'D:/Backup_folder/Logs'

if __name__ == "__main__":
    # Usage
    backup_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/", log, 7)
    delete_empty_folders(destination,log)
    delete_expired_files(log)
    backup_containers(destination,log)

```

## Dependencies

1. `Python 3`
2. `psycopg2`

