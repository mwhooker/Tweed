import json
import restclient


class Bitly:
    format='json'
    version='2.0.1'
    base_url='http://api.bit.ly'

    def __init__(self, login, apiKey):
        self.login=login
        self.apiKey=apiKey

        self.stdParams = "?version=%s&login=%s&apiKey=%s" % (
                self.version, self.login, self.apiKey)

    def shorten(self, url):
        '''
        http://api.bit.ly/shorten
            ?version=2.0.1&longUrl=<url>&login=<login>&apiKey=<api key>
        '''
        endpoint = "%s/shorten%s&longUrl=%s" % (self.base_url, self.stdParams, url)
        res = json.loads(restclient.GET(endpoint, async=False))
        if res['statusCode'] != "OK":
            raise Exception(res['errorMessage'])

        return res['results'][url]['shortUrl']

        
