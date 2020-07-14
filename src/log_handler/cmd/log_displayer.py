from datetime import datetime
from time import time
from kafka import KafkaConsumer
import configparser

import sys
sys.path.append('../')
from internal.parse_log import parse_log_line


g_display_interval = 10

def display_log():
    print('--- HTTP LOG MONITOR ---')
    print('--- ' + datetime.now().strftime('%X'))

    while True:
        l_display = parse_queue_line(time())
        if 'section' in l_display.keys():
            l_display_string = '{time:%X} - Top section since {display_interval} seconds : {section}' \
                            '\n\tSection hits: {hits} \n\tPercentage of traffic: {percentage}%' \
                            '\n\tTotal hits: {total_hits}'.format(**l_display)
        else:
            l_display_string = '{time:%X} - ¯\\_(ツ)_/¯ No traffic since ' \
                            '{display_interval} seconds'.format(**l_display)
        print(l_display_string)

def parse_queue_line(p_time):
    l_sections = {}
    l_time_delta = 0
    for c_message in g_consumer:
        try:
            l_parsed_line = parse_log_line(c_message.value.decode('utf-8'))
        except ValueError:
            continue
        l_section = l_parsed_line['section']
        if l_section not in l_sections.keys():
            l_sections[l_section] = 1
        else:
            l_sections[l_section] += 1
        l_time_delta = time() - p_time
        if l_time_delta >= g_display_interval:
            break

    l_time = datetime.now()
    l_res_display = {
        'time': l_time,
        'display_interval': int(l_time_delta)
    }

    if l_sections != {}:
        l_max_section = max(l_sections, key=l_sections.get)
        l_total_hits = sum(l_sections.values())
        l_section_hits = l_sections[l_max_section]
        l_res_display['section'] = l_max_section
        l_res_display['hits'] = l_section_hits
        l_res_display['percentage'] = round(l_section_hits/ l_total_hits * 100)
        l_res_display['total_hits'] = l_total_hits

    return l_res_display


if __name__ == '__main__':
    g_config = configparser.ConfigParser()
    g_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_bootstrap_servers = g_config['KAFKA']['bootstrap_servers']
    g_logs_queue = g_config['KAFKA']['logs_queue']
    g_consumer = KafkaConsumer(g_logs_queue, bootstrap_servers=[g_bootstrap_servers],
        consumer_timeout_ms=1000,
        group_id='log')
    display_log()