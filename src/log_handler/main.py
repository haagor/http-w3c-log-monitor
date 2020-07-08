import configparser
import queue
import threading
import log_reader
import log_displayer


if __name__ == '__main__':
    l_config = configparser.ConfigParser()
    l_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_log_file_path = l_config['READER']['log_file']
    l_queue = queue.Queue()
    l_thread_displayer = threading.Thread(target=log_displayer.display_log, args=([l_queue]))
    l_thread_displayer.start()
    print('hello')
    l_thread_reader = threading.Thread(target=log_reader.read_file, args=([g_log_file_path, l_queue]))
    l_thread_reader.start()
