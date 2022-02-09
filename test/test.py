import unittest

from data.info.test_info import TestInfo

def suite():
    test_suite = unittest.TestSuite()

    # data/info
    print('==> data.info')
    test_suite.addTest(TestInfo('test_load_info'))
    test_suite.addTest(TestInfo('test_balance'))
    test_suite.addTest(TestInfo('test_cashflow'))
    test_suite.addTest(TestInfo('test_income'))    
    test_suite.addTest(TestInfo('test_all_info'))    

    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
