import tweepy
import time
from keys import keys

CONSUMER_KEY = keys['cons_key']
CONSUMER_SECRET = keys['cons_sec']
ACCESS_KEY = keys['acc_key']
ACCESS_SECRET = keys['acc_sec']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME= 'last_seen_kanyeid.txt'
totalTime = 0
timeSinceLastTweet = 0

def tellKanyeVeryCool():
    print('Waiting for kanye..')

    def retrieve_last_seen_id(file_name):
        f_read = open(file_name, 'r')
        last_seen_id = int(f_read.read())
        f_read.close()
        return last_seen_id

    def store_last_seen_id(last_seen_id, file_name):
        f_write = open(file_name, 'w')
        f_write.write(str(last_seen_id))
        f_write.close()
        return

    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    kanye = api.user_timeline(screen_name = 'kanyewest', since_id=last_seen_id, tweet_mode='extended')

    for kTweet in reversed(kanye):
        print(str(kTweet.id) + ' - ' + kTweet.full_text)
        last_seen_id = kTweet.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if 'RT @' not in kTweet.full_text:
            print('New Kanye Tweet')
            print('Thanks, Kanye!')
            api.update_status('@kanyewest Thank you Kanye, very cool!', kTweet.id)
            timeSinceLastTweet = 0

while True:
    tellKanyeVeryCool()
    totalTime += 15
    timeSinceLastTweet += 15
    print ('Seconds since last tweet : ' + str(timeSinceLastTweet - 15))
    print ('Searched for ' + str(totalTime - 15) + ' seconds.')
    time.sleep(15)
