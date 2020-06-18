#author: HankHuge
import configparser
import time

class TwitterAuth:
    def __init__(self):
        conf = configparser.RawConfigParser()

        # Put your twitter secrets in file "Secrets.properties"
        conf.read("Secrets.properties")
        
        # Api keys
        self.API_KEY = conf.get('TWITTER_AUTH_SEC', 'API_KEY')
        self.API_KEY_SECRET = conf.get('TWITTER_AUTH_SEC', 'API_KEY_SECRET')
        # Access token keys
        self.ACCESS_TOKEN = conf.get('TWITTER_AUTH_SEC', 'ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = conf.get('TWITTER_AUTH_SEC', 'ACCESS_TOKEN_SECRET')


from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

# Class for Stream listening(It continuesly listens for new tweets)
class TListener(StreamListener):
    def on_data(self, raw_data):

        global start_time, tweets_file

        tweets_file.write(raw_data)

        if(time.time() - start_time > 3):
            print("Times Up! Exiting....")
            tweets_file.close()
            exit(0)
        return True
    
    def on_error(self, status_code):
        print(status_code)

def main():
    listener = TListener()
    Tauth = TwitterAuth()
    auth = OAuthHandler(Tauth.API_KEY, Tauth.API_KEY_SECRET)
    auth.set_access_token(Tauth.ACCESS_TOKEN, Tauth.ACCESS_TOKEN_SECRET)
    
    stream = Stream(auth, listener)

    word_list = []
    global start_time, tweets_file

    
    with open('related_words') as f:
        s = f.read()
        word_list = list(map(lambda x: x.strip(), s.split(',')))
        f.close()
    tweets_file = open(r'tweets.json', 'w')

    start_time = time.time()
    stream.filter(track=word_list)
    

if __name__ == '__main__':
    main()