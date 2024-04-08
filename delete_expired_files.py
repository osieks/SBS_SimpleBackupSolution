import os
import datetime
import psycopg2

# secret data from local file
import secret

def delete_expired_files(log_dir):
    log =""
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user=secret.username, password=secret.password)
    cur = conn.cursor()

    # Get the current date and time
    now = datetime.datetime.now()

    # Fetch records where date_of_delete is older than now
    cur.execute("SELECT path, name FROM public.backed_up WHERE date_of_delete < %s", (now,))
    records = cur.fetchall()

    for record in records:
        path, name = record
        file_path = os.path.join(path, name)

        # Check if the file exists and delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
            log = log+f"Deleted file: {file_path}\n"

        # Update the path in the database to be empty
        cur.execute("UPDATE public.backed_up SET path = '' WHERE path = %s AND name = %s", (path, name))

    conn.commit()
    cur.close()
    conn.close()
    log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
    with open(log_dir+"\\delete_expired_files_log_"+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".txt", "w") as text_file:
        text_file.write(log)

