import unittest

from unittest.mock import patch
from rss_feed_reader import read_envs


class TestReadEnvVariables(unittest.TestCase):
    @patch.dict('os.environ', {'HOW_DEEP_ITEMS_LOOK_BACK': '1', 'LOOKING_DAYS': '91', 'SENSITIVE_PLUGINS': 'git'})
    def test_read_existing_envs(self):
        result = read_envs()
        self.assertNotEqual(result, 'One or more env variable missed')

    @patch.dict('os.environ', {'LOOKING_DAYS': '91', 'SENSITIVE_PLUGINS': 'git'})
    def test_read_missed_envs(self):
        with self.assertRaises(SystemExit) as cm:
            read_envs()

        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
