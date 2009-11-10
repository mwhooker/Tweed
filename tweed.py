import sys
import twitter
import logging
import ConfigParser


class Tweed:

    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.log = logging.getLogger('tweed')
        self.log.info("init")

        config = ConfigParser.SafeConfigParser()
        try:
            config.read('config.cfg')
        except config.ParsingError:
            self.log.error("uh oh parsing error!")

        self.api_handle = twitter.Api(
                username=config.get('Twitter User', 'screen_name'), 
                password=config.get('Twitter User', 'password')
                )

    def close_friend_gap(self):
        friends = set([i.id for i in self.api_handle.GetFriends()])
        followers = set([i.id for i in self.api_handle.GetFollowers()])

        to_follow = followers.difference(friends)

        if to_follow:
            self.log.info('found %d people to follow', len(to_follow))
            for i in to_follow:
                self.log.info('following %s', i.screen_name)
                self.api_handle.CreateFriendship(i.id)



