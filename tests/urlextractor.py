import unittest
from urlextract import UrlExtractor

class NoUrl(unittest.TestCase):
    url = 'asfla aflksdlk sdakfasdfk  www. sa'
    
    def setUp(self):
        self.extractor = UrlExtractor(self.url)

    def testHasUrl(self):
        self.assertFalse(self.extractor.hasUrl())

    def testUrlCount(self):
        self.assertEqual(self.extractor.urlsFound(), 0)



class SingleUrl(unittest.TestCase):
    url = 'http://docs.python.org/library/unittest.html'
    
    def setUp(self):
        self.extractor = UrlExtractor("garbage %s trash" % self.url)

    def testHasUrl(self):
        self.assert_(self.extractor.hasUrl())

    def testUrlCount(self):
        self.assertEqual(self.extractor.urlsFound(), 1)

    def testGetUrl(self):
        self.assert_(self.url in self.extractor.urlList())
    


class MultiUrl(unittest.TestCase):
    urls = ['http://docs.python.org/library/unittest.html',
            'http://effbot.org/zone/python-list.htm']
    
    def setUp(self):
        self.extractor = UrlExtractor(' trash '.join(self.urls))

    def testHasUrl(self):
        self.assert_(self.extractor.hasUrl())

    def testUrlCount(self):
        self.assertEqual(self.extractor.urlsFound(), 2)

    def testGetUrl(self):
        for i in self.urls:
            self.assert_(i in self.extractor.urlList())


'''
class All(unittest.TestSuite):
    def __init(self):
        self.addTest(NoUrl)
        self.addTest(SingleUrl)
        self.addTest(MultiUrl)
'''
