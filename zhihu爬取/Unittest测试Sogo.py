import unittest
from selenium import webdriver


class TestSogo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get('https://www.sogo.com/')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_001(self):
        self.assertEqual(self.driver.title, u'搜狗搜索引擎 - 上网从搜狗开始')

    def test_002(self):
        self.assertTrue(self.driver.find_element_by_id('query').is_enabled())

    def test_003(self):
        self.assertTrue(self.driver.current_url, 'https://www.sogo.com/')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSogo)
    unittest.TextTestRunner(verbosity=2).run(suite)
