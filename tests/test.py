import unittest
from unittest.mock import Mock
from check import Check
from functional import K2Functional, RSFunctional


class TestCheck(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCheck, self).__init__()
        self.k2 = K2Functional()
        self.rs = RSFunctional()
        self.k2.send_code = Mock()
        self.k2.com = Mock()
        self.k2.com.close = Mock()

    def runTest(self):
        self.test_access_check_normal()
        self.test_access_check_no_rs_connection()
        self.test_access_check_no_k2_connection()


    def test_access_check_normal(self):
        check = Check(self.k2, self.rs)
        check.pause = Mock()
        self.k2.com.readline = Mock(return_value='f=152.6489 МГц'.encode('cp866'))
        check.access_check()
        self.assertEqual(check.f, 152.650)


    def test_access_check_no_rs_connection(self):
        check = Check(self.k2, self.rs)
        check.pause = Mock()
        message = ''
        self.k2.com.readline = Mock(return_value='f=000.0010 МГц'.encode('cp866'))
        try:
            check.access_check()
        except Exception as exc:
            message = str(exc)
        self.assertEqual(message, 'Нет связи с радиостанцией. Проверьте питание и PTT')


    def test_access_check_no_k2_connection(self):
        check = Check(self.k2, self.rs)
        check.pause = Mock()
        message = ''
        self.k2.com.readline = Mock(return_value=''.encode('cp866'))
        try:
            check.access_check()
        except Exception as exc:
            message = str(exc)
        self.assertEqual(message, 'Нет связи с К2-82. Проверьте подключение и активность УСТ и ДУ')



if __name__ == '__main__':
    unittest.main()