import os
import datetime
import psycopg2

# secret data from local file
import secret

debug = 0

def delete_expired_files(log_file):
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
            if debug==1: print(f"Deleted file: {file_path}")
            log = log+f"Deleted file: {file_path}\n"

        # Update the path in the database to be empty
        cur.execute("UPDATE public.backed_up SET path = '' WHERE path = %s AND name = %s", (path, name))

    conn.commit()
    cur.close()
    conn.close()
    log=log+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"\n"
    with open(log_file, "a", encoding="utf-8") as text_file:
        text_file.write(log)

