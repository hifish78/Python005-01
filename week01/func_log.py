import datetime
import logging
import os
import time

# PATH_BASE = "/var/log/"
PATH_BASE = "/Users/ayu/"
LOG_FILE_NAME = "func.log"


# Solution#1
def log_time():
    cur_time = time.strftime("%Y-%m-%d %X", time.localtime())
    cur_date = cur_time.split()[0]
    log_file_path = os.path.join(PATH_BASE, cur_date)
    if not os.path.exists(log_file_path):
        os.mkdir((log_file_path))
    try:
        log_file = open(os.path.join(log_file_path, LOG_FILE_NAME), "a")
        log_file.write(cur_time + "\n")
    except BaseException:
        print(f"Failed to open file: {log_file}")
    finally:
        log_file.close()

# Solution#2
def func_invoke_time():
    cur_date = time.strftime("%Y-%m-%d")
    log_file_path = os.path.join(PATH_BASE, cur_date)
    if not os.path.exists(log_file_path):
        os.mkdir((log_file_path))

    file_name = os.path.join(log_file_path, LOG_FILE_NAME)
    logging.basicConfig(filename=file_name,
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s::%(message)s')

    logging.info("The function is invoked")

if __name__ == "__main__":
    # log_time()
    func_invoke_time()
