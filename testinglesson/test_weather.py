import unittest
from unittest.mock import patch
from weather import get_temperature

class TestWeather(unittest.TestCase):
    
    @patch('weather.requests.get')
    def test_get_temperature(self,mock_get):
        mock_get.return_value.json.return_value = {'temp':25}
        result = get_temperature('nairobi')
        self.assertEqual(result,25)

if __name__ == '__main__':
    unittest.main()