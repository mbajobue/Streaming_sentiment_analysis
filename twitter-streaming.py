from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys

consumer_key = '-'
consumer_secret = '-'
access_token = '-'
access_secret = '-'


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'] )
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    l = StdOutListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    print(api.me().name)

    stream = Stream(auth, l)
    print("Filter term: "+sys.argv[1])
    stream.filter(track=[sys.argv[1]])
