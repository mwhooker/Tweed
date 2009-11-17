import unittest, re, os

def get_tests():
    loader = unittest.TestLoader()

    names = [i[0:-3] for i in os.listdir(
        os.path.dirname(os.path.abspath(__file__))) 
        if re.match('^test.+\.py$', i)]
    return loader.loadTestsFromNames(names)

def main():
    suite = get_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)



if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tweed')
    main()
