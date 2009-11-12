import sys
import twitter
import logging
import ConfigParser
from feed import Feed
from urlextract import UrlExtractor


class Tweed:

    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.log = logging.getLogger('tweed')
        self.log.info("init")

        config = ConfigParser.SafeConfigParser()
        try:
            config.read('../conf/config.cfg')
        except config.ParsingError:
            self.log.error("uh oh parsing error!")

        self.twitter = twitter.Api(
                username=config.get('Twitter User', 'screen_name'), 
                password=config.get('Twitter User', 'password')
                )

    def close_friend_gap(self):
        friends = set([i.id for i in self.twitter.GetFriends()])
        followers = set([i.id for i in self.twitter.GetFollowers()])

        to_follow = followers.difference(friends)

        if to_follow:
            self.log.info('found %d people to follow', len(to_follow))
            for i in to_follow:
                self.log.info('following %s', i.screen_name)
                self.twitter.CreateFriendship(i.id)

    def get_feed_requests(self, since_id=None):
        requests = self.twitter.GetDirectMessages(since_id=since_id)

        dms = []
        if requests:
            valid_requests = [i for i in requests if UrlExtractor(i.text).hasUrl()]
            self.log.info('found %d new feed requests', len(valid_requests))
            for i in valid_requests:
                self.log.info('got dm from %s', i.sender_screen_name)
                dm = Feed(
                        i.id, i.sender_id, i.created_at_in_seconds,
                        UrlExtractor(i.text).urlList()[0]
                        )
                dms.append(dm)

        return dms if dms else None

