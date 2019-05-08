from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys

consumer_key = 'kuY85oTUo1yFhYTLGyT2xN7jn'
consumer_secret = 'u5nbGVP7km2upSj1Z7HwZcfIPDawbWEEi1kfwZYUANEITSHcEH'
access_token = '1102997194976698369-V9vctOm55DWi3lsyypNHukmO9dWXZx'
access_secret = 'PEmwC6mR1tNyCiF3b7nTfijrAlgh0kyGse5pZ80wM2pzc'


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
