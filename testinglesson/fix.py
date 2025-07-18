import unittest

# Import all three modules that make up our app
from user_loader import load_users
from user_filter import filter_active_users
from user_report import generate_report

class TestIntegration(unittest.TestCase):

    def test_user_reporting_pipeline(self):
        # Step 1: Load raw user data (simulate loading from database/file)
        users = load_users()

        # Step 2: Filter only active users
        active_users = filter_active_users(users)

        # Step 3: Generate report from filtered users
        report = generate_report(active_users)

        # Final step: Assert the result of the full process
        # If Alice and Charlie are active, report should mention them only
        self.assertEqual(report, "Active Users: Alice, Charlie")

        # Explanation:
        # This test integrates the entire pipeline:
        # load_users -> filter_active_users -> generate_report
        # If any part is broken, this test will fail.
        # For example, if filter_active_users has a bug, this test catches it.
    
    def test_with_no_active_users(self):
        # Simulate a failure case: no users are active
        inactive_data = [
            {"id": 1, "name": "X", "active": False},
            {"id": 2, "name": "Y", "active": False}
        ]

        # Instead of calling load_users, use the simulated data directly
        active_users = filter_active_users(inactive_data)
        report = generate_report(active_users)

        self.assertEqual(report, "Active Users: ")

if __name__ == '__main__':
    unittest.main()
