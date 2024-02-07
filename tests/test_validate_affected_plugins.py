import unittest
import datetime
from rss_feed_reader import validate_affected_plugins


class TestValidateAffectedPlugins(unittest.TestCase):
    def test_validate_affected_plugins(self):
        sensitive_plugins = ['Git server', 'saml']
        affected_plugins = ['Git server', 'kubernetes']
        expected_detected_plugins = ['Git server']
        actually_detected_plugins = validate_affected_plugins(sensitive_plugins, affected_plugins)

        self.assertEqual(actually_detected_plugins, expected_detected_plugins)

    def test_validate_non_affected_plugins(self):
        sensitive_plugins = ['kubernetes', 'saml']
        affected_plugins = ['Matrix Project', 'Analysis Model API']
        expected_detected_plugins = []
        actually_detected_plugins = validate_affected_plugins(sensitive_plugins, affected_plugins)

        self.assertEqual(actually_detected_plugins, expected_detected_plugins)


if __name__ == '__main__':
    unittest.main()
