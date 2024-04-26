Aplication for defining data backups, retention, schedule(not yet implemented) etc.


# Backup and Cleanup Script

This project contains Python scripts for backing up files, deleting expired files, and removing empty folders.

## Scripts

1. `backup_files.py`: This script backs up files from a source directory to a destination directory. It also logs the backup process.

2. `delete_expired_files.py`: This script deletes files that have passed their retention period.

3. `delete_empty_folders.py`: This script removes any empty folders in a given directory.

## Usage

Change source, destination and log paths.

```python
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
```

## Dependencies

1. `Python 3`
2. `psycopg2`

