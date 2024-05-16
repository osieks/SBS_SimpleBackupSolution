import shutil
import os
import time
import datetime
import psycopg2

# secret data from local file
import secret
import delete_expired_files
import delete_empty_folders

def backup_files(src_dir, dest_dir,log_dir, retention_days):
    log =''
    # Check if both the source and destination directories exist
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        log=log+f"Source directory {src_dir} does not exist.\n"
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir+"/")

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user=secret.username, password=secret.password)
    cur = conn.cursor()

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
            backup_files(src_dir+file+"/", dest_dir+file+"/",log_dir, retention_days)
            
        else:
            print(f"File: {file}")
            log=log+f"File: {file}\n"
            file_mod = time.ctime(os.path.getmtime(src_dir+file))
            print(file_mod)
            log=log+f"{file_mod}\n"
            
            # Construct full file path
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            
            # Check if the file modified is in the database
            cur.execute("SELECT path,name FROM public.backed_up WHERE file_modified = %s AND name = %s", (file_mod,file,))
            result = cur.fetchone()
            
            print("Searching for last modified in database...")
            print(result)
            print("datetime now: ")
            print(datetime.datetime.now())
            
            if result is not None:
                # If the file modified is in the database, move the old file to the new place
                old_path = result[0]
                shutil.move(old_path+file, dest_dir+file)
                
                print("dziwny dest_dir")
                print(dest_dir)
                # Update the file record in the database
                cur.execute("UPDATE public.backed_up SET date_of_backup = %s, date_of_delete = %s, path = %s WHERE file_modified = %s AND name = %s", (datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir, file_mod, file))
                
                print((datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir, file_mod, file))
            else:
                # Copy the file to the destination directory
                shutil.copy(src_file, dest_file)
                
                # Insert the file record into the database
                cur.execute("INSERT INTO public.backed_up (name, date_of_backup, file_modified, date_of_delete, path) VALUES (%s, %s, %s, %s, %s)", (file, datetime.datetime.now(),file_mod,datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir))
            
            conn.commit()
            
    cur.close()
    conn.close()
            
    log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
    with open(log_dir+"\\log_"+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".txt", "w") as text_file:
        text_file.write(log)
    



if __name__ == "__main__":
    source = 'D:/Source_folder/'
    destination = 'D:/Backup_folder/'
    log = 'D:\Backup_folder\Logs'
    # Usage
    backup_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/", log, 7)