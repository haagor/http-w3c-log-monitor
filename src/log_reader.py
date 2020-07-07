import configparser
from os import SEEK_END


def read_file(p_file):
    with open(p_file, 'r') as c_file:
        while True:
            l_line = c_file.readline()
            if not l_line:
                continue
            else:
                try:
                    print(l_line)
                    #parsed_line = self.parse_log_line(l_line)
                    #self.input_queue.put(parsed_line)
                    #self.input_traffic_queue.put(parsed_line['datetime'])
                except LineFormatError:
                    break


config = configparser.ConfigParser()
config.read('../config.ini')
g_log_file_path = config['READER']['log_file']
read_file(g_log_file_path)