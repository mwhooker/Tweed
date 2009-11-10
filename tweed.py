import twitter
import logging


class Tweed:

    def __init__(self):
        self.log = logging.getLogger('tweed')
        logging.basicConfig()
        self.api_handle = twitter.Api(username="tweediebot", password="NasP&8Eceh")
        self.log.info("init")

    def close_friend_gap(self):
        friends = set(self.api_handle.GetFriends())
        followers = set(self.api_handle.GetFollowers())

        to_follow = followers.difference(friends)

        if to_follow == True:
            self.log.info('found ' + len(to_follow) + ' people to follow')
            for i in to_follow:
                self.log.info('following ' + i.screen_name);
                self.api_handle.CreateFriendship(i.id)



