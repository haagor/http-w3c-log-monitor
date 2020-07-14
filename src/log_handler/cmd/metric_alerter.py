from datetime import datetime
from time import time
import threading
import configparser
from kafka import KafkaConsumer


g_traffic = []
g_alert_interval = 120
g_alert_raised = False

def run_alerting():
    l_thread_alert = threading.Thread(target=check_alert)
    l_thread_alert.start()

    while True:
        refresh_metrics()
        l_time_delta = time()
        for c_message in g_consumer:
            g_traffic.append(datetime.strptime(c_message.value.decode('utf-8'), '%m/%d/%Y, %H:%M:%S'))
            if (time() - l_time_delta) >= 1:
                break

def refresh_metrics():
    l_time = datetime.now()
    for c_line in g_traffic:
        if (l_time - c_line).total_seconds() > g_alert_interval:
            g_traffic.remove(c_line)
        else:
            return

def check_alert():
    global g_alert_raised
    l_request_threshold = float(g_request_threshold_by_second)

    while True:
        l_hits = len(g_traffic)
        if l_hits / g_alert_interval <= l_request_threshold and g_alert_raised:
            print('RECOVERED High traffic generated an alert - hits = ' + str(l_hits) + ' , triggered at ' + datetime.now().strftime('%H:%M:%S'))
            g_alert_raised = False
        if l_hits / g_alert_interval > l_request_threshold and not g_alert_raised:
            print('High traffic alert - hits = ' + str(l_hits) + ' , triggered at ' + datetime.now().strftime('%H:%M:%S'))
            g_alert_raised = True


if __name__ == '__main__':
    g_config = configparser.ConfigParser()
    g_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_request_threshold_by_second = g_config['ALERTER']['request_threshold_by_second']
    g_bootstrap_servers = g_config['KAFKA']['bootstrap_servers']
    g_metrics_queue = g_config['KAFKA']['metrics_queue']
    g_consumer = KafkaConsumer(g_metrics_queue, bootstrap_servers=[g_bootstrap_servers],
        consumer_timeout_ms=1000,
        group_id='log')
    run_alerting()