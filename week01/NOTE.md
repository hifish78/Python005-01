学习笔记
solution2:
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
