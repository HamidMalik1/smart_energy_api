import unittest

from smart_energy_api import solaredge_api as s

class SolaredgeApiSideEffects(unittest.TestCase):
    def test_solaredgemeters_meterdata(self):
        d = s.solaredgemeters.meterdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_siteenergy_energydata(self):
        d = s.siteenergy.energydata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_sitepower_powerdata(self):
        d = s.sitepower.powerdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_overview_site_overview(self):
        d = s.overview.site_overview()
        print(d)
        self.assertIsInstance(d, dict)


    def test_siteenergydetails_energydetailsdata(self):
        d = s.siteenergydetails.energydetailsdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_sitepoweflow_powerflowdata(self):
        d = s.sitepowerflow.powerflowdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_sitestorage_storagedata(self):
        d = s.sitestorage.storagedata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_siteenvbenefits_envdata(self):
        d = s.siteenvbenefits.envdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_siteinverter_inverterdata(self):
        d = s.siteinverter.inverterdata()
        print(d)
        self.assertIsInstance(d, dict)


    def test_sitesensors_sensordata(self):
        d = s.sitesensors.sensordata()
        print(d)
        self.assertIsInstance(d, dict)

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