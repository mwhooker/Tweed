import twitter
import logging


class Tweed:

    def __init__(self):
        self.log = logging.getLogger('tweed')
        api_handle = twitter.Api(username="tweediebot", password="NasP&8Eceh")

    def close_friend_gap(self):
        friends = set(self.api.GetFriends())
        followers = set(self.api.GetFollowers())

        to_follow = followers.difference(friends)

        if to_follow == True:
            self.log.info('found ' + len(to_follow) + ' people to follow')
            for i in to_follow:
                self.log.info('following ' + i.screen_name);
                self.api.CreateFriendship(i.id)



