import datetime
import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/events")

    def test_add_correct_data(self):
        response = requests.put(
            self.app_path, json={"date": "2022-03-01", "event": "Dzień Balearów"}
        )
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsInstance(response_json["id"], int)
        self.assertIsInstance(response_json["date_added"], str)

        date_added = datetime.date.fromisoformat(response_json["date_added"])
        self.assertGreaterEqual(
            date_added, datetime.date.today() - datetime.timedelta(days=1)
        )
        self.assertLessEqual(
            date_added, datetime.date.today() + datetime.timedelta(days=1)
        )


if __name__ == "__main__":
    unittest.main()