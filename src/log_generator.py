import configparser
import threading
from datetime import datetime
from random import choice, randint, uniform
from string import ascii_lowercase
from time import strftime, gmtime, ctime


def generate_line():
    l_comment = ''
    if randint(0,100) == 0:
        l_comment = '#'
    l_http_request = choice(['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS'])
    l_http_status = str(randint(1,6)) + '00'
    l_reponse_bytes = str(randint(100, 10000))
    l_datetime = datetime.now().strftime('%d/%b/%Y:%X') + ' ' + strftime("%z", gmtime())
    l_res_line = l_comment \
           + 'hostname' + ' ' \
           + generate_word(6) + ' ' \
           + generate_word(6) + ' ' \
           + '[' + l_datetime + ']' + ' ' \
           + '"' + l_http_request + ' ' \
           + generate_url() + ' ' \
           + 'HTTP/1.1"' + ' ' \
        + l_http_status + ' ' \
           + l_reponse_bytes + '\n'
    return l_res_line

def generate_word(p_length):
    return ''.join(choice(ascii_lowercase) for i in range(p_length))

def generate_url():
    l_url = choice(['/', 'http://my.site.com/pages', 'http://my.site.com/home'])
    if l_url != '/':
        l_url += generate_sub_url()
    return l_url

def generate_sub_url():
    l_depth = randint(0, 4)
    if l_depth == 0:
        return '/'

    l_sub_url = ''
    for c_i in range(l_depth):
        l_sub_url += '/' + generate_word(randint(3, 10))

    l_sub_url += choice(['.php', '.html', ''])
    return l_sub_url

def periodic_generator():
    try:
        g_log_file.write(generate_line())
        g_log_file.flush()
    except ValueError as e:
        print(e)
        g_log_file.close()
    threading.Timer(g_request_by_second, periodic_generator).start()


config = configparser.ConfigParser()
config.read('../config.ini')
g_log_file_path = config['LOG_GENERATOR']['log_file']
g_request_by_second = config['LOG_GENERATOR']['request_by_second']
g_request_by_second = 1 / int(g_request_by_second)

with open(g_log_file_path, 'w') as c_file:
    g_log_file = open(g_log_file_path, 'w')
    periodic_generator()
