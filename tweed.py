import sys
import twitter
import logging


class Tweed:

    def __init__(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.log = logging.getLogger('tweed')
        self.log.info("init")

        self.api_handle = twitter.Api(username="tweediebot", password="NasP&8Eceh")

    def close_friend_gap(self):
        friends = set([i.id for i in self.api_handle.GetFriends()])
        followers = set([i.id for i in self.api_handle.GetFollowers()])

        to_follow = followers.difference(friends)

        if to_follow:
            self.log.info('found %d people to follow', len(to_follow))
            for i in to_follow:
                self.log.info('following %s', i.screen_name)
                self.api_handle.CreateFriendship(i.id)



