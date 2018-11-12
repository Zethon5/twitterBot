import tweepy
import time
import random
from keys import keys                                                     #This will import users specific keys from their own key.py file
print('Turning Twitter Bot On.')


totalTime = 0                                                             # This will be so you can keep track of how long the program has been on
CONSUMER_KEY = keys['cons_key']
CONSUMER_SECRET = keys['cons_sec']
ACCESS_KEY = keys['acc_key']
ACCESS_SECRET = keys['acc_sec']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)                 # THIS IS ESSENTIALLY A LOG IN FOR THE PROGRAM TO AUTHENTICATE THE TWITTER ACCOUNT FOR USE
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

fileName= 'last_seen_id.txt'                                              # THIS PULLS A FILE CONTAINING THE LAST TWEET THAT TRIGGERED THE BOT AS A SORT OF SAVE TO MOVE ON FROM THIS POINT.

#api.update_status('Hello bot on.')                                       # Sends out a tweet whenever the script is started.

#api.create_friendship(screen_name = '')                                  # WORKS!          Just don't include the @ in their @ name.
#api.send_direct_message_new(screen_name ='' , text = 'Hello friend!')    # DOESNT WORK!    Trying to pull the user like above, doesn't seem to work. Possibly removed dm feature from tweepy.

goodResponses = ['Hi, how are you?', 'Hello!', 'Hello, how are you?', 'You Called?', 'Hi!', "How's it going?",'How are you doing today?']
happyResponses = ["I'm great!", "I'm doing well!", "It's a great day to be a bot!", "I am good, how are you?"]
spanishResponses = ['Hola!', 'Que pasa?', 'Como estas?']

def replyToTweets():
    print('searching for tweets..')

    def retrieveLastSeenID(fileName):                                 # THIS OPENS THE FILE WITH THE LAST ID
        f_read = open(file_name, 'r')
        last_seen_id=int(f_read.read().strip())
        f_read.close()
        return last_seen_id

    def storeLastSeenID(last_seen_id, fileName):                      # IF THE BOT RESPONDS TO A TWEET, IT SAVES THE ID TO BE REFERENCED
        f_write = open(fileName, 'w')                                    # LATER SO IT DOESNT RESPOND TO THE SAME TWEET MORE THAN ONCE.
        f_write.write(str(lastSeenID))
        f_write.close()
        return

    lastSeenID = retrieveLastSeenID(fileName)              
    mentions = api.mentions_timeline(
                                lastSeenID,
                                tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + str(mention.full_text))
        lastSeenID = mention.id
        storeLastSeenID(lastSeenID, fileName)
        #THESE ARE THE HOW ARE YOU RESPONSES
        if 'how are you' in mention.full_text.lower() or 'it going' in mention.full_text.lower() or 'it goin' in mention.full_text.lower() or 'it hanging' in mention.full_text.lower() or 'how are ya' in mention.full_text.lower():
            print('pyBot Called.')
            print('pyBot Responding.')
            api.update_status('@' + mention.user.screen_name + ' ' +  random.choice(happyResponses), mention.id )
            api.create_favorite(mention.id)
        #THESE ARE THE HELLO RESPONSES BACK.
        elif 'hello' in mention.full_text.lower() or 'hey' in mention.full_text.lower() or 'hi' in mention.full_text.lower() or "what's up" in mention.full_text.lower() or 'sup' in mention.full_text.lower():
            print('pyBot Called.')
            print('pyBot Responding.')
            api.update_status('@' + mention.user.screen_name + ' ' +  random.choice(goodResponses), mention.id )
            api.create_favorite(mention.id)
        #THESE ARE THE 'SPANISH' RESPONSES. DOESNT SUPPORT ACCENTS OR UPSIDE DOWN CHARACTERS.
        elif 'hola' in mention.full_text.lower():
            print('pyBot Called.')
            print('pyBot Responding.')
            api.update_status('@' + mention.user.screen_name + ' ' +  random.choice(spanishResponses), mention.id )
            api.create_favorite(mention.id)

while True:                         #This is the endless loop that just runs the programs until force stopped.
    replyToTweets()
    totalTime += 15
    print('Search for ' + str(totalTime - 15) + ' seconds')          # I do the -15 to get rid of the original 15 seconds..otherwise it would be 
    time.sleep(15)                                                   # 15 seconds more than the actual time. 
