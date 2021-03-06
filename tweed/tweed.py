import sys
import logging
from feed import Feed
from urlextract import UrlExtractor


class Tweed:
    '''Main mediator between twitter and the application'''

    TWITTER_SOURCE = "Tweed"

    def __init__(self, twitterApi, urlShortener):
        self.urlShortener = urlShortener
        self.twitter = twitterApi
        self.twitter.SetSource(self.TWITTER_SOURCE)
        self.log = logging.getLogger('tweed')

    def close_friend_gap(self):
        '''Make sure Tweed follows everyone that follows Tweed
        Todo: 1. save on API calls by caching # of followers.'''
        try:
            twit_followers = self.twitter.GetFollowers()
            friends = set([i.id for i in self.twitter.GetFriends()])
            followers = set([i.id for i in twit_followers])

            diff_ids = followers.difference(friends)
            to_follow = [i for i in twit_followers if i.id in diff_ids]


            if to_follow:
                self.log.info('found %d people to follow', len(to_follow))
                for i in to_follow:
                    self.log.info('following %s', i.screen_name)
                    self.twitter.CreateFriendship(i.id)
        except Exception as e:
            self.log.error(e)

    def get_feed_requests(self, since_id=None):
        '''Have any new people requested Tweed follow a feed?
        If so, return a list of Feed objects'''
        try:
            requests = self.twitter.GetDirectMessages(since_id=since_id)
        except Exception as e:
            self.log.error(e)
            return None

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
            url = self.urlShortener.shorten(i.link)

            if feed_title:
                title = " from \"%s\"" % (feed_title)

            message = "new post%s: %s \"%s\"" % (title, url, i.title)[0:140]
            self.twitter.PostDirectMessage(user_id, message)


