
import sys, tweepy
from app import db,User
import os
from dotenv import load_dotenv


## class to load twitter data
class load_data:
    def twitter_auth(self):
        try:
            consumer_key = os.getenv('API_KEY')
            consumer_secret = os.getenv('API_SECRET')
            access_token = os.getenv('ACCESS_TOKEN')
            access_secret = os.getenv('ACCESS_SECRET')
        except KeyError:
            sys.stderr.write("Twitter environment variable not set")
            sys.exit(1)
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_secret)
        return auth

    def get_twitter_client(self):
        auth = self.twitter_auth()
        client = tweepy.API(auth, wait_on_rate_limit=True)
        return client

    ## function that loads data into sqlite database 
    def load_twitter_dat(self,user):
        client = self.get_twitter_client()
        for status in tweepy.Cursor(client.user_timeline,screen_name=user).items():
            user = User(id = status.id,tweet=status.text,created_date=status.created_at)
            db.session.add(user)
        db.session.commit()





