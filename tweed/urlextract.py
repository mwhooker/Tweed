import re

class UrlExtractor:

    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    #need to convert this to pythonese
    #pattern = '^(?P<Protocol>?:(?:ht|f)tp(?:s?)\:\/\/|~\/|\/)?(?P<Username:Password>?:\w+:\w+@)?(?P<Subdomains>?:(?:[-\w]+\.)+(?P<TopLevel Domains>?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?P<Port)(?::[\d]{1,5})?(?P<Directories>?:(?:(?:\/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?P<Query>?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?P<Anchor>?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$'

    
    def __init__(self, string):
        valid = re.compile(self.pattern)
        self.result = valid.findall(string)

    def hasUrl(self):
        return bool(self.result)

    def urlsFound(self):
        return len(self.result) if self.result else False

    def urlList(self):
        return self.result

