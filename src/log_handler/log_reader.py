import configparser
import re
from datetime import datetime
import queue


def read_file(p_file, p_queue):
    with open(p_file, 'r') as c_file:
        while True:
            l_line = c_file.readline()
            if not l_line:
                continue
            else:
                l_parsed_line = parse_log_line(l_line)
                p_queue.put(l_parsed_line)
                #self.input_traffic_queue.put(parsed_line['datetime'])


def parse_log_line(p_line):
    l_pattern = re.compile(
        r'^(?P<remote_host>\S*) (?P<user_identity>\S*) (?P<user_name>\S*) \[(?P<datetime>.*?)\]'
        r' \"(?P<request>.*)\" (?P<status_code>\d*) (?P<response_size>\d*)$'
    )
    l_matching_pattern = l_pattern.match(p_line)
    l_formatted_line = l_matching_pattern.groupdict()
    l_formatted_line['response_size'] = int(l_formatted_line['response_size'])
    l_formatted_line['status_code'] = int(l_formatted_line['status_code'])
    l_formatted_line['section'] = get_section(l_formatted_line['request'])
    l_formatted_line['datetime'] = datetime.strptime(l_formatted_line['datetime'][0:20], '%d/%b/%Y:%X')
    return l_formatted_line

def get_section(p_request):
    l_section = p_request.split(' ')

    if l_section[1] == '/':
        return '/'

    l_section = l_section[1].split('/')
    l_res = '/'.join(l_section[0:4])
    return l_res
