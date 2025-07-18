import unittest
from user_loader import load_users
from user_filter import filter_active_users
from user_report import generate_report

class TestIntergration(unittest.TestCase):
    
    def test_user_reporting_pipeline(self):
        users = load_users()
        active_users = filter_active_users(users)
        report = generate_report(active_users)
        
        self.assertEqual(report,"Active Users: Alice, Charlie")
        
    def test_with_no_active_users(self):
        inactive_data = [
            {"id": 1, "name": "X", "active": False},
            {"id": 2, "name": "Y", "active": False}
        ]
        
        active_users = filter_active_users(inactive_data)
        report = generate_report(active_users)
        
        self.assertEqual(report,"Active Users: ")

if __name__ == '_main__':
    unittest.main()
        