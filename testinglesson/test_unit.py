import unittest
from user_loader import load_users
from user_filter import filter_active_users
from user_report import generate_report

class TestUnit(unittest.TestCase):
    
    def test_load_users(self):
        users = load_users()
        self.assertEqual(len(users),3)
        self.assertTrue(any(user['active']for user in users))
    
    def test_filter_active_users(self):
        data = [
            {"id": 1, "active": True},
            {"id": 2, "active": False}
        ]
        result = filter_active_users(data)
        self.assertEqual(len(result),1)
        self.assertTrue(result[0]["active"])
    
    def test_generate_report(self):
        users = [{"name": "Alice"}, {"name": "Charlie"}]
        report = generate_report(users)
        self.assertEqual(report,"Active Users: Alice, Charlie")

if __name__ == "__main__":
    unittest.main()
    
    