import unittest

def get_tests():
    loader = unittest.TestLoader()

    return loader.loadTestsFromName('urlextractor')

def main():
    suite = get_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)



if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')
    main()
