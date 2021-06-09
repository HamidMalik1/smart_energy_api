import unittest

TEST_CONFIG = {
	'ilmanet': {
		'url': 'https://ilmanet.fi'
	}
}

class IlmanetSideEffects(unittest.TestCase):
	def test_fetch(self):
		from smart_energy_api import bcdc_fmi as m
		f = m.fetch(TEST_CONFIG['ilmanet']['url'])

		self.assertEqual(f.status, 200)
		self.assertEqual(f.headers.get('Content-Type'), 'text/csv; charset=utf-8')


class Ilmanet(unittest.TestCase):
	def test_lines(self):
		from io import BytesIO
		from smart_energy_api import bcdc_fmi as m
		buffer = BytesIO('a,b,c\n1,2,3\r\n3,4,5'.encode('utf-8'))
		l = m.lines(buffer)

		self.assertEqual(len(l), 3)
		self.assertEqual(l[1], '1,2,3')


if __name__ == '__main__':
    unittest.main()
