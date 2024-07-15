import logging
from unittest.mock import patch
import pytest
from rss_feed_reader import custom_exception  # replace with your specific import

@patch('logging.Logger.error')
def test_custom_exception(mock_error):
    # Given
    expected_first_message = 'Something wrong wuth the RSS endpoint: https://www.jenkins.io/security/advisories/rss.xml'  # replace with your feed url
    expected_second_message = 'Please check an access to the RSS endpoint and try again'
    expected_third_message = 'Script abnormal tetminated'

    # When
    with pytest.raises(SystemError):
        custom_exception()

    # Then
    assert mock_error.call_args_list[0].args[0] == expected_first_message
    assert mock_error.call_args_list[1].args[0] == expected_second_message
    assert mock_error.call_args_list[2].args[0] == expected_third_message