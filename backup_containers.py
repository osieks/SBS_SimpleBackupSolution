import subprocess
import datetime

debug = 1

def backup_containers(destination,log_file):
    log = ""
    #docker import img.tar my-new-image:latest

    output = subprocess.getoutput("docker ps --format '{{.Names}}")
    if debug==1:
        print(output)

    output=output.replace("'", "")
    containers_list = list(output.split("\n"))

    for container_name in containers_list:
        output = subprocess.getoutput(f"docker export --output {destination}\{container_name}.tar {container_name}")
        if debug==1:
            print(container_name)
            print(f"docker export --output {destination}\{container_name}.tar {container_name}")
            print(output)
        
        log = log + output +"\n"
        log = log + f"exported {container_name}" +"\n"
    with open(log_file, "a", encoding="utf-8") as text_file:
        text_file.write(log)

if __name__ == "__main__":
    destination = 'D:/Backup_folder/'
    log = 'D:\Backup_folder\Logs\logi_testowe.txt'

    backup_containers(destination,log)