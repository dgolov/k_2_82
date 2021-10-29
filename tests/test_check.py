import random, unittest
from unittest.mock import Mock
from PyQt5.QtWidgets import QMessageBox
from check import Check
from functional import K2Functional, RSFunctional


def input_check_class(function):
    """ Декоратор подключающий объект класса Check к тестируемым функциям
        :param function: - тестируемая функция
    """

    def create_check_object(self, *args, **kwargs):
        self.check = Check(self.k2, self.rs)
        self.check.pause = Mock()
        self.check.event_log = Mock()
        function(self, *args, **kwargs)

    return create_check_object


def input_check_tx_functions(function):
    """ Декоратор создает фейковое поведение вызываемых функций при тестировании функции проверки передатчика
        :param function: - тестируемая функция
    """

    def create_mock_functions(self, *args, **kwargs):
        self.check.f = 151.825
        self.check.access_check = Mock()
        self.check.power_check = Mock()
        self.check.get_check_status = Mock()
        self.check.modulation_input_sensitivity_check = Mock()
        self.check.harmonic_distortion_check = Mock()
        self.check.max_deviation_check = Mock()
        self.check.frequency_deviation_check = Mock()
        self.k2.connect_com_port = Mock(return_value=True)
        function(self, *args, **kwargs)

    return create_mock_functions


class TestCheck(unittest.TestCase):

    def setUp(self):
        self.k2 = K2Functional()
        self.rs = RSFunctional()
        self.check = Check(self.k2, self.rs)
        self.k2.send_code = Mock()
        self.k2.numbers_entry = Mock()
        self.k2.com = Mock()
        self.k2.com.close = Mock()

    @input_check_tx_functions
    def test_check_transmitter_normal(self):
        self.k2.check_deviation = True
        self.check.check_transmitter()

        self.assertTrue(self.check.access_check.assert_called)
        self.assertTrue(self.check.power_check.assert_called)
        self.assertTrue(self.check.modulation_input_sensitivity_check.assert_called)
        self.assertTrue(self.check.harmonic_distortion_check.assert_called)
        self.assertTrue(self.check.max_deviation_check.assert_called)
        self.assertTrue(self.check.frequency_deviation_check.assert_called)
        self.assertEqual(self.check.chm_u['value'], 9.5)
        self.assertTrue(self.check.chm_u['is_correct'])
        self.assertEqual(self.check.i['value'], 50)
        self.assertTrue(self.check.i['is_correct'])

    @input_check_tx_functions
    def test_check_transmitter_off_check_max_deviation(self):
        self.k2.check_deviation = False
        random.randint = Mock(return_value=490)
        self.check.check_transmitter()

        self.assertTrue(self.check.max_deviation_check.assert_not_called)
        self.assertEqual(self.check.chm_max['value'], 4.9)
        self.assertTrue(self.check.chm_max['is_correct'])

    @input_check_tx_functions
    def test_check_transmitter_altavia(self):
        self.k2.model = 'Альтавия'
        self.check.check_transmitter()

        self.assertEqual(self.check.chm_u['value'], 15)
        self.assertTrue(self.check.chm_u['is_correct'])
        self.assertEqual(self.check.i['value'], 40)
        self.assertTrue(self.check.i['is_correct'])

    @input_check_tx_functions
    def test_check_transmitter_icom(self):
        self.k2.model = 'Icom'

        self.check.check_transmitter()

        self.assertEqual(self.check.chm_u['value'], 16)
        self.assertTrue(self.check.chm_u['is_correct'])
        self.assertEqual(self.check.i['value'], 70)
        self.assertTrue(self.check.i['is_correct'])

    @input_check_tx_functions
    def test_check_transmitter_radiy(self):
        self.k2.model = 'Радий'

        self.check.check_transmitter()

        self.assertEqual(self.check.high_p['value'], '-')
        self.assertTrue(self.check.high_p['is_correct'])

    @input_check_tx_functions
    def test_check_transmitter_rn(self):
        self.k2.model = 'РН 311М'

        self.check.check_transmitter()

        self.assertEqual(self.check.p['value'], '-')
        self.assertTrue(self.check.p['is_correct'])
        self.assertEqual(self.check.i['value'], 110)
        self.assertTrue(self.check.i['is_correct'])

    @input_check_class
    def test_access_check_normal(self):
        self.k2.com.readlines = Mock(return_value=['f=152.6489 МГц '.encode('cp866')])
        self.check.access_check()
        self.assertEqual(self.check.f, 152.650)

    @input_check_class
    def test_access_check_no_rs_connection(self):
        message = ''
        self.k2.com.readlines = Mock(return_value=['f=000.0010 МГц '.encode('cp866'), ])
        try:
            self.check.access_check()
        except Exception as exc:
            message = str(exc)
        self.assertEqual(message, 'Нет связи с радиостанцией. Проверьте питание и PTT')

    @input_check_class
    def test_access_check_no_k2_connection(self):
        message = ''
        self.k2.com.readlines = Mock(return_value=''.encode('cp866'))
        try:
            self.check.access_check()
        except Exception as exc:
            message = str(exc)
        self.assertEqual(message, 'Нет связи с К2-82. Проверьте подключение и активность УСТ и ДУ')

    @input_check_class
    def test_power_check_low_normal(self):
        self.k2.com.readlines = Mock(return_value=['P= 2.13   Вт '.encode('cp866')])
        QMessageBox.information = Mock()
        self.check.power_check()
        self.assertEqual(self.check.p['value'], 2.13)
        self.assertTrue(self.check.p['is_correct'])
        self.assertEqual(self.check.high_p['value'], '-')
        self.assertTrue(self.check.high_p['is_correct'])

    @input_check_class
    def test_power_check_low_few_value(self):
        self.k2.com.readlines = Mock(return_value=['P= 1.54   Вт '.encode('cp866')])
        QMessageBox.information = Mock()
        self.check.power_check()
        self.assertEqual(self.check.p['value'], 1.54)
        self.assertFalse(self.check.p['is_correct'])
        self.assertEqual(self.check.high_p['value'], '-')
        self.assertTrue(self.check.high_p['is_correct'])

    @input_check_class
    def test_power_check_high_normal(self):
        self.k2.com.readlines = Mock(return_value=['P= 5.12   Вт '.encode('cp866'), ])
        QMessageBox.information = Mock()
        self.check.power_check()
        self.assertEqual(self.check.p['value'], '-')
        self.assertTrue(self.check.p['is_correct'])
        self.assertEqual(self.check.high_p['value'], 5.0)
        self.assertTrue(self.check.high_p['is_correct'])

    @input_check_class
    def test_power_check_all_normal(self):
        self.k2.com.readlines = Mock(return_value=['P= 5.12   Вт '.encode('cp866'), 'P= 2.61   Вт '.encode('cp866')])
        QMessageBox.information = Mock()
        self.check.power_check()
        self.assertEqual(self.check.p['value'], 2.61)
        self.assertTrue(self.check.p['is_correct'])
        self.assertEqual(self.check.high_p['value'], 5.0)
        self.assertTrue(self.check.high_p['is_correct'])

    @input_check_class
    def test_modulation_input_sensitivity_check(self):
        self.check.chm_u['value'] = 9.5
        self.k2.com.readlines = Mock(return_value=['ЧМ+= 3.01  мВ '.encode('cp866'), ])
        self.check.modulation_input_sensitivity_check()
        self.assertEqual(self.check.chm_u['value'], 9.5)
        self.assertTrue(self.check.chm_u['is_correct'])

    @input_check_class
    def test_harmonic_distortion_check_normal(self):
        self.k2.com.readlines = Mock(return_value=['Kг= 1.01  % '.encode('cp866'), ])
        self.check.harmonic_distortion_check()
        self.assertEqual(self.check.kg['value'], 1.01)
        self.assertTrue(self.check.kg['is_correct'])

    @input_check_class
    def test_harmonic_distortion_check_not_correct(self):
        self.k2.com.readlines = Mock(return_value=['Kг= 3.01  % '.encode('cp866'), ])
        self.check.harmonic_distortion_check()
        self.assertEqual(self.check.kg['value'], 3.01)
        self.assertFalse(self.check.kg['is_correct'])

    @input_check_class
    def test_max_deviation_check_normal(self):
        self.k2.com.readlines = Mock(return_value=['ЧМмах= 4.92   мВ '.encode('cp866'), ])
        self.check.harmonic_distortion_check()
        self.assertEqual(self.check.chm_max['value'], 4.92)
        self.assertTrue(self.check.chm_max['is_correct'])

    @input_check_class
    def test_max_deviation_check_not_correct(self):
        self.k2.com.readlines = Mock(return_value=['ЧМмах= 5.23   мВ '.encode('cp866'), ])
        self.check.harmonic_distortion_check()
        self.assertEqual(self.check.chm_max['value'], 5.23)
        self.assertFalse(self.check.chm_max['is_correct'])

    @input_check_class
    def test_max_deviation_check_no_data(self):
        self.k2.com.readlines = Mock(return_value=[])
        self.check.harmonic_distortion_check()
        self.assertEqual(self.check.chm_max['value'], '-')
        self.assertTrue(self.check.chm_max['is_correct'])

    @input_check_class
    def test_frequency_deviation_check_normal(self):
        self.check.f = 151.825
        self.k2.com.readlines = Mock(return_value=['Отклонение= 0.213   Гц '.encode('cp866')])
        self.check.frequency_deviation_check()
        self.assertEqual(self.check.dev['value'], 213)
        self.assertTrue(self.check.dev['is_correct'])

    @input_check_class
    def test_frequency_deviation_check_not_correct(self):
        self.check.f = 151.825
        self.k2.com.readlines = Mock(return_value=['Отклонение= 0.853   Гц '.encode('cp866')])
        self.check.frequency_deviation_check()
        self.assertEqual(self.check.dev['value'], 853)
        self.assertFalse(self.check.dev['is_correct'])

    def test_noise_reduction_decrypt_normal(self):
        mock_line = ['Kг= 25.01  % ', 'U= 2.3   В ']
        # self.k2.numbers_entry = Mock()
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 25
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 24)
        self.assertTrue(flag)
        self.assertTrue(self.check.noise_reduction['is_correct'])
        self.assertTrue(self.k2.numbers_entry.assert_called)

    def test_noise_reduction_decrypt_with_kg_99_presents(self):
        mock_line = ['Kг= 99.0  % ', 'U= 2.3   В ']
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 18
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 19)
        self.assertFalse(flag)

    def test_noise_reduction_decrypt_with_big_u_value(self):
        mock_line = ['Kг= 25.01  % ', 'U= 22.3   В ']
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 18
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 18)
        self.assertFalse(flag)

    def test_noise_reduction_decrypt_with_u_2_volts(self):
        mock_line = ['Kг= 25.01  % ', 'U= 2.0   В ']
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 18
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 18)
        self.assertFalse(flag)

    def test_noise_reduction_decrypt_with_u_milli_volts(self):
        mock_line = ['Kг= 25.01  % ', 'U= 2.0  мВ ']
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 18
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 18)
        self.assertFalse(flag)

    def test_noise_reduction_decrypt_not_correct(self):
        mock_line = ['Kг= 25.01  % ', 'U= 2.3   В ']
        self.k2.com.readlines = Mock(return_value=mock_line)
        flag, noise_reduction = True, 10
        for line in mock_line:
            if flag:
                flag, noise_reduction = self.check.noise_reduction_decrypt(flag, line, noise_reduction)
        self.assertEqual(noise_reduction, 10)
        self.assertFalse(flag)
        self.assertFalse(self.check.noise_reduction['is_correct'])

    def test_get_serial_number(self):
        self.k2.model = 'Motorola'
        self.rs.connect_com_port = Mock(return_value=True)
        self.rs.get_serial = Mock(return_value='672TQUM2433')
        sn = self.check.get_serial_number()
        self.assertEqual(sn, '672TQUM2433')


if __name__ == '__main__':
    unittest.main()
