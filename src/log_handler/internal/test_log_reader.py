import unittest
from datetime import datetime

from parse_log import parse_log_line
from parse_log import get_section


class TestStringMethods(unittest.TestCase):

	def test_get_section(self):
		section = get_section('GET http://my.site.com/pages/ HTTP/1.1')
		self.assertEqual(section, 'http://my.site.com/pages')

		section = get_section('GET http://my.site.com/pages/jdhaddjovy/nkjtp/fyvinleuqr/miymjekgfn HTTP/1.1')
		self.assertEqual(section, 'http://my.site.com/pages')

		section = get_section('GET / HTTP/1.1')
		self.assertEqual(section, '/')

	def test_parse_log_line(self):
		parsed_line = parse_log_line(
			'hostname zwkivs ojsbrx [08/Jul/2020:08:10:30 +0000] "GET http://my.site.com/home/ HTTP/1.1" 600 1375')
		expected_parsed_line = {
		'remote_host': 'hostname',
		'user_identity': 'zwkivs',
		'user_name': 'ojsbrx',
		'datetime': datetime(2020, 7, 8, 8, 10, 30),
		'request': 'GET http://my.site.com/home/ HTTP/1.1',
		'status_code': 600,
		'response_size': 1375,
		'section': 'http://my.site.com/home'
		}
		self.assertDictEqual(parsed_line, expected_parsed_line)

		parsed_line = parse_log_line(
			'hostname pttmsb scibil [08/Jul/2020:08:10:29 +0000] "HEAD / HTTP/1.1" 300 1002')
		expected_parsed_line = {
		'remote_host': 'hostname',
		'user_identity': 'pttmsb',
		'user_name': 'scibil',
		'datetime': datetime(2020, 7, 8, 8, 10, 29),
		'request': 'HEAD / HTTP/1.1',
		'status_code': 300,
		'response_size': 1002,
		'section': '/'
		}
		self.assertDictEqual(parsed_line, expected_parsed_line)

		parsed_line = parse_log_line(
			'hostname pttmsb scibil [08/Jul/2020:08:10:29 +0000] "HEAD / HTTP/1.1" 300 1002')
		expected_parsed_line = {
		'remote_host': 'hostname',
		'user_identity': 'pttmsb',
		'user_name': 'scibil',
		'datetime': datetime(2020, 7, 8, 8, 10, 19),
		'request': 'HEAD / HTTP/1.1',
		'status_code': 300,
		'response_size': 1002,
		'section': 'http://my.site.com/home'
		}
		self.assertNotEqual(parsed_line, expected_parsed_line)


if __name__ == '__main__':
    unittest.main()