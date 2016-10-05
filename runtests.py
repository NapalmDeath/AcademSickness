import os
import unittest


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(CURRENT_DIR, 'tests')


def create_suite():
    return unittest.TestLoader().discover(TEST_DIR, pattern='*.py')


if __name__ == '__main__':
   suite = create_suite()

   runner = unittest.TextTestRunner()
   runner.run(suite)