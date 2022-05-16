import datetime
import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/events")

    def test_retrieve_is_list(self):
        create_response = requests.put(
            self.app_path, json={"date": "2022-03-21", "event": "Pierwszy dzień wiosny"}
        )
        self.assertEqual(create_response.status_code, 200)

        retrieve_response = requests.get(self.app_path + "/2022-03-21")

        self.assertEqual(retrieve_response.status_code, 200)
        response_json = retrieve_response.json()
        self.assertIsInstance(response_json, list)


if __name__ == "__main__":
    unittest.main()