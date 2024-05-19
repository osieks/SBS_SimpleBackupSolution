import shutil
import os
import time
import datetime
import psycopg2

# secret data from local file
import secret
import delete_expired_files
import delete_empty_folders

debug = 0

def backup_files(src_dir, dest_dir,log_file, retention_days):

    print(f"backing up {src_dir}")
    try:
        log =''
        # Check if both the source and destination directories exist
        if not os.path.exists(src_dir):
            if debug==1: print(f"Source directory {src_dir} does not exist.")
            log=log+f"Source directory {src_dir} does not exist.\n"
            return
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir+"/")

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user=secret.username, password=secret.password)
        cur = conn.cursor()

        # List all files in the source directory
        files = os.listdir(src_dir)
        if debug==1: print(files)

        for file in files:
            #if debug==1: print(src_dir+file)
            
            if(os.path.isdir(src_dir+file)):
                if debug==1: print(f"Recursing directory: {file}")
                log=log+f"Recursing directory: {file}\n"
                if not os.path.exists(dest_dir+file+"/"):
                    os.makedirs(dest_dir+file+"/")
                if debug==1: print(src_dir+file+"/")
                backup_files(src_dir+file+"/", dest_dir+file+"/",log_file, retention_days)
                
            else:
                if debug==1: print(f"File: {file}")
                log=log+f"File: {file}\n"
                file_mod = time.ctime(os.path.getmtime(src_dir+file))
                if debug==1: print(file_mod)
                log=log+f"{file_mod}\n"
                
                # Construct full file path
                src_file = os.path.join(src_dir, file)
                dest_file = os.path.join(dest_dir, file)
                
                # Check if the file modified is in the database
                cur.execute("SELECT path,name FROM public.backed_up WHERE file_modified = %s AND name = %s", (file_mod,file,))
                result = cur.fetchone()
                
                if debug==1: print("Searching for last modified in database...")
                if debug==1: print(result)
                if debug==1: print("datetime now: ")
                if debug==1: print(datetime.datetime.now())
                log=log+f"Searching for last modified in database...\n"
                log=log+f"{result}\n"
                log=log+f"datetime now: \n"
                log=log+f"{datetime.datetime.now()}\n"
                
                if result is not None:
                    # If the file modified is in the database, move the old file to the new place
                    old_path = result[0]
                    shutil.move(old_path+file, dest_dir+file)

                    # Update the file record in the database
                    cur.execute("UPDATE public.backed_up SET date_of_backup = %s, date_of_delete = %s, path = %s WHERE file_modified = %s AND name = %s", (datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir, file_mod, file))
                    
                    if debug==1: print((datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir, file_mod, file))
                else:
                    # Copy the file to the destination directory
                    shutil.copy(src_file, dest_file)
                    
                    # Insert the file record into the database
                    cur.execute("INSERT INTO public.backed_up (name, date_of_backup, file_modified, date_of_delete, path) VALUES (%s, %s, %s, %s, %s)", (file, datetime.datetime.now(),file_mod,datetime.datetime.now()+datetime.timedelta(days=retention_days), dest_dir))
                
                conn.commit()
                
        cur.close()
        conn.close()
                
        log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
        with open(log_file, "a", encoding="utf-8") as text_file:
            text_file.write(log)
        print("Done!")
        
    except Exception as e:
        print(e)



if __name__ == "__main__":
    source = 'D:/Source_folder/'
    destination = 'D:/Backup_folder/'
    log = 'D:\Backup_folder\Logs'
    # Usage
    backup_files(source, destination+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"/", log, 7)