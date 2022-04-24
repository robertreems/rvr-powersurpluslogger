import unittest
import mock
# from main import Average, read_meters_enery_delivered, send_notification, \
#     is_no_power_notification_send
import main
from exceptions import HomeWizzardCommunication


class TestRun(unittest.TestCase):
    # 4th line = Meter Reading electricity delivered to client (Tariff 1) in 0,001 kWh
    # 5th line = Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh
    # 6th line = Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh
    # 7th line = Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh
    example_HW_return = b'/XMX5XMXABCE000030057\
        \r\n\
        \r\\n0-0:96.1.1(39383239353535372020202020202020)\
        \r\n1-0:1.8.1(15422.201*kWh)\
        \r\n1-0:1.8.2(13272.006*kWh)\
        \r\n1-0:2.8.1(03335.474*kWh)\
        \r\n1-0:2.8.2(07612.880*kWh)\
        \r\n0-0:96.14.0(0001)\
        \r\n1-0:1.7.0(0003.96*kW)\
        \r\n1-0:2.7.0(0000.00*kW)\
        \r\n0-0:96.13.1()\
        \r\n0-0:96.13.0()\
        \r\n!'

    def test_Average(self):
        data = [1, 2, 3]
        result = main.Average(data)
        self.assertEqual(result, 2)

    @mock.patch('requests.get')
    def test_read_meters_enery_delivered_success(self, mock_requests_get):
        mock_requests_get().status_code = 200
        mock_requests_get().content = self.example_HW_return

        tariff1, tariff2 = main.read_meters_enery_delivered()

        self.assertEqual(tariff1, 3335.474)
        self.assertEqual(tariff2, 7612.88)

    @mock.patch('requests.get')
    def test_read_meters(self, mock_requests_get):
        mock_requests_get().status_code = 200
        mock_requests_get().content = self.example_HW_return

        tariff1, tariff2 = main.read_meters_enery_delivered()

        self.assertEqual(tariff1, 3335.474)
        self.assertEqual(tariff2, 7612.88)

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
