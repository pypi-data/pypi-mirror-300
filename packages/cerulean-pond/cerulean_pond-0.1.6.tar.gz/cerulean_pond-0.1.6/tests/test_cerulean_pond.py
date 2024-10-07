import unittest
from cerulean_pond import Data_Pond

class TestCeruleanPond(unittest.TestCase):
    def test_authentication(self):
        dp = Data_Pond()
        self.assertFalse(dp.authenticated)

if __name__ == "__main__":
    unittest.main()
