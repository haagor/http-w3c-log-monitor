import unittest
from src import log_reader

class TestStringMethods(unittest.TestCase):

	def test_get_section(self):
		section = log_reader.get_section('GET http://my.site.com/pages/ HTTP/1.1')
		self.assertEqual(section, 'http://my.site.com/pages')

		section = log_reader.get_section('GET http://my.site.com/pages/jdhaddjovy/nkjtp/fyvinleuqr/miymjekgfn HTTP/1.1')
		self.assertEqual(section, 'http://my.site.com/pages')

		section = log_reader.get_section('GET / HTTP/1.1')
		self.assertEqual(section, '/')


if __name__ == '__main__':
    unittest.main()