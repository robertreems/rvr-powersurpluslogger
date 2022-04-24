import unittest
import mock
# from main import Average, read_meters_enery_delivered, send_notification, \
#     is_no_power_notification_send
import main
from exceptions import HomeWizzardCommunication


class TestRun(unittest.TestCase):
    def test_Average(self):
        data = [1, 2, 3]
        result = main.Average(data)
        self.assertEqual(result, 2)

    @mock.patch('requests.get')
    def test_read_meters_enery_delivered_success(self, mock_requests_get):
        mock_requests_get().status_code = 200
        mock_requests_get().content = b'garbage\n\
garbage\n\
garbage\n\
garbage\n\
garbage\n\
----------000000001----\n\
----------000000015----\n\
'

        tariff1, tariff2 = main.read_meters_enery_delivered()

        self.assertEqual(tariff1, 1.0)
        self.assertEqual(tariff2, 15.0)

    @mock.patch('requests.get')
    def test_read_meters_enery_delivered_fail(self, mock_requests_get):
        mock_requests_get().status_code = 404

        with self.assertRaises(HomeWizzardCommunication):
            main.read_meters_enery_delivered()

    @mock.patch('requests.get')
    def read_meters_enery_delivered_unknown_error(self, mock_requests_get):
        mock_requests_get().status_code = 1234

        with self.assertRaises(HomeWizzardCommunication):
            main.read_meters_enery_delivered()

    # Notification should be send 1th time at no power.
    @mock.patch('rvrbase.rvrlogger.Rvrlogger.log_application_event')
    # @mock.patch('main.is_no_power_notification_send', False)
    def test_send_notification_1(self, mock_rvrlogger):

        main.send_notification([0, 0, 0, 0])

        mock_rvrlogger.assert_called()

        # The global var is_no_power_notification_send should be set to True.
        self.assertTrue(main.is_no_power_notification_send)

    # Notification should not be send if already send.
    @mock.patch('rvrbase.rvrlogger.Rvrlogger.log_application_event')
    @mock.patch('main.is_no_power_notification_send', True)
    def test_send_notification_2(self, mock_rvrlogger):

        main.send_notification([0, 0, 0, 0])

        mock_rvrlogger.assert_not_called()

        # The global var is_no_power_notification_send should be set to True.
        self.assertTrue(main.is_no_power_notification_send)

    # Notification should be send if a lot of power is produced.
    @mock.patch('rvrbase.rvrlogger.Rvrlogger.log_application_event')
    @mock.patch('main.is_no_power_notification_send', True)
    def test_send_notification_3(self, mock_rvrlogger):

        main.send_notification([300, 300, 300])

        mock_rvrlogger.assert_called()

        # The global var is_no_power_notification_send should be set to false.
        self.assertFalse(main.is_no_power_notification_send)

    # Notification should not be send if a lot of power is produced and
    # is_no_power_notification_send is set to false
    @mock.patch('rvrbase.rvrlogger.Rvrlogger.log_application_event')
    @mock.patch('main.is_no_power_notification_send', False)
    def test_send_notification_4(self, mock_rvrlogger):

        main.send_notification([300, 300, 300])

        mock_rvrlogger.assert_not_called()

        # The global var is_no_power_notification_send should be set to false.
        self.assertFalse(main.is_no_power_notification_send)


if __name__ == '__main__':
    unittest.main()
