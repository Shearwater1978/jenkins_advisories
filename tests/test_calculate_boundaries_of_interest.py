import unittest
import datetime
from rss_feed_reader import calculate_boundaries_of_interest

class TestCalculateBoundariesOfInterest(unittest.TestCase):
    def test_boundaries_of_interest(self):
        SHORT_DATE_FORMAT= "%Y-%m-%d"
        till_date, from_date = calculate_boundaries_of_interest(7)
        # till_date should be should be today
        expected_till_date = datetime.datetime.today().strftime(SHORT_DATE_FORMAT)
        self.assertEqual(till_date, expected_till_date)

        # from_date 7 days before today
        expected_from_date = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime(SHORT_DATE_FORMAT)
        self.assertEqual(from_date, expected_from_date)

if __name__ == '__main__':
    unittest.main()
