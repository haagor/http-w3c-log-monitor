from datetime import datetime
from time import time
from kafka import KafkaConsumer
from kafka import KafkaProducer
import configparser

import sys
sys.path.append('../')
from internal.parse_log import parse_log_line

def consume_log():
    while True:
        for c_message in g_consumer:
            try:
                l_parsed_line = parse_log_line(c_message.value.decode('utf-8'))
            except ValueError:
                continue
            produce_metric(l_parsed_line['datetime'])

def produce_metric(p_line):
    g_producer.send(g_metrics_queue, bytes(p_line.strftime("%m/%d/%Y, %H:%M:%S"), 'utf-8'))


if __name__ == '__main__':
    g_config = configparser.ConfigParser()
    g_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_bootstrap_servers = g_config['KAFKA']['bootstrap_servers']
    g_logs_queue = g_config['KAFKA']['logs_queue']
    g_consumer = KafkaConsumer(g_logs_queue, bootstrap_servers=[g_bootstrap_servers],
        consumer_timeout_ms=1000,
        group_id='metric')

    g_metrics_queue = g_config['KAFKA']['metrics_queue']
    g_producer = KafkaProducer(bootstrap_servers = g_bootstrap_servers)
    consume_log()
