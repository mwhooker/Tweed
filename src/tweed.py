import sys
import logging
from feed import Feed
from urlextract import UrlExtractor


class Tweed:

    def __init__(self, twitterApi, urlshortener):
        self.urlshortener = urlshortener
        self.twitter = twitterApi
        self.log = logging.getLogger('tweed')

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

    def notify_followers(self, user_id, posts, feed_title=''):
        for i in posts:
            self.log.info( "notifying %d of post %s", user_id, i.title)
            url = self.urlshortener.shorten(i.link)

            if feed_title:
                title = " from \"%s\"" % (feed_title)

            message = "new post%s: %s \"%s\"" % (title, url, i.title)[0:140]
            #self.twitter.PostDirectMessage(user_id, message)
            self.log.info(message)


