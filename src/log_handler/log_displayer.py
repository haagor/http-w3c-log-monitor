from datetime import datetime
from time import time


g_display_interval = 10

def display_log(p_queue):
    print('--- HTTP LOG MONITOR ---')
    print('--- ' + datetime.now().strftime('%X'))

    l_display_time = time()
    while True:
        l_time_delta = time() - l_display_time
        if l_time_delta >= g_display_interval:
            l_display = parse_queue_line(p_queue)
            if 'section' in l_display.keys():
                l_display_string = '{time:%X} - Top section since {display_interval} seconds : {section}' \
                                '\n\tSection hits: {hits} \n\tPercentage of traffic: {percentage}%' \
                                '\n\tTotal hits: {total_hits}'.format(**l_display)
            else:
                l_display_string = '{time:%X} - ¯\\_(ツ)_/¯ No traffic since ' \
                                '{display_interval} seconds'.format(**l_display)
            l_display_time = time()
            print(l_display_string)

def parse_queue_line(p_queue):
    l_sections = {}
    while not p_queue.empty():
        l_parsed_line = p_queue.get()
        l_section = l_parsed_line['section']
        if l_section not in l_sections.keys():
            l_sections[l_section] = 1
        else:
            l_sections[l_section] += 1

    l_time = datetime.now()
    l_res_display = {
        'time': l_time,
        'display_interval': g_display_interval
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