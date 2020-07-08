import configparser
import queue
import threading

import log_reader
import log_displayer
import alerter


if __name__ == '__main__':
    g_config = configparser.ConfigParser()
    g_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_log_file_path = g_config['READER']['log_file']
    g_request_threshold_by_second = g_config['ALERTER']['request_threshold_by_second']
    g_queue = queue.Queue()
    g_queue_metric = queue.Queue()
    g_thread_displayer = threading.Thread(target=log_displayer.display_log, args=([g_queue]))
    g_thread_displayer.start()
    g_thread_alerter = threading.Thread(target=alerter.run_alerting, args=([g_queue_metric, g_request_threshold_by_second]))
    g_thread_alerter.start()
    g_thread_reader = threading.Thread(target=log_reader.read_file, args=([g_log_file_path, g_queue, g_queue_metric]))
    g_thread_reader.start()
