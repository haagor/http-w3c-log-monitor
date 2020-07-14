from kafka import KafkaProducer
import configparser


def read_file(p_file):
    with open(p_file, 'r') as c_file:
        while True:
            l_line = c_file.readline()
            if not l_line:
                continue
            else:
                producer(l_line)

def producer(p_line):
    g_producer.send(g_logs_queue, bytes(p_line.strip(), 'utf-8')) #there is a chance to send \n in the line


if __name__ == '__main__':
    g_config = configparser.ConfigParser()
    g_config.read('/home/haag/workspace/http-w3c-log-monitor/config.ini')
    g_bootstrap_servers = g_config['KAFKA']['bootstrap_servers']
    g_logs_queue = g_config['KAFKA']['logs_queue']
    g_producer = KafkaProducer(bootstrap_servers = g_bootstrap_servers)
    g_log_file_path = g_config['READER']['log_file']

    read_file(g_log_file_path)