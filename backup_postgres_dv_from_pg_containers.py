import subprocess
import datetime

debug = 1

def backup_postgres_dv_from_pg_containers(destination,log_file):
    log = ""
    #docker import img.tar my-new-image:latest

    output = subprocess.getoutput("docker ps --filter ancestor=postgres --format '{{.Names}}")
    if debug==1:
        print(output)

    output=output.replace("'", "")
    containers_list = list(output.split("\n"))

    for container_name in containers_list:
        # docker exec -u postgres cool_merkle pg_dump -Fc postgres > D:\Backup_folder\db2.dump
        output = subprocess.getoutput(f"docker exec -u postgres {container_name} pg_dump -Fc postgres > {destination}\{container_name}_backup.dump ")
        if debug==1:
            print(container_name)
            print(f"docker exec -u postgres {container_name} pg_dump -Fc postgres > {destination}\{container_name}_backup.dump ")
            print(output)
        
        log = log + output +"\n"
        log = log + f"exported {container_name}'s database" +"\n"
    with open(log_file, "a", encoding="utf-8") as text_file:
        text_file.write(log)


if __name__ == "__main__":
    destination = 'D:/Backup_folder/'
    log = 'D:\Backup_folder\Logs\logi_testowe.txt'

    backup_postgres_dv_from_pg_containers(destination,log)