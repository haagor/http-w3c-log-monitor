from datetime import datetime
from time import time
import threading


g_traffic = []
g_alert_interval = 120
g_alert_raised = False

def run_alerting(p_queue_metric, p_request_threshold_by_second):
    l_thread_alert = threading.Thread(target=check_alert, args=([p_request_threshold_by_second]))
    l_thread_alert.start()

    while True:
        refresh_metrics()
        while not p_queue_metric.empty():
            g_traffic.append(p_queue_metric.get())

def refresh_metrics():
    l_time = datetime.now()
    for c_line in g_traffic:
        if (l_time - c_line).total_seconds() > g_alert_interval:
            g_traffic.remove(c_line)
        else:
            return

def check_alert(p_request_threshold_by_second):
    global g_alert_raised
    l_request_threshold = float(p_request_threshold_by_second)

    while True:
        if len(g_traffic) / g_alert_interval <= l_request_threshold and g_alert_raised:
            print(datetime.now().strftime('%H:%M:%S') + ' - ALERT RECOVER traffic too high')
            g_alert_raised = False
        if len(g_traffic) / g_alert_interval > l_request_threshold and not g_alert_raised:
            print(datetime.now().strftime('%H:%M:%S') + ' - ALERT traffic too high')
            g_alert_raised = True