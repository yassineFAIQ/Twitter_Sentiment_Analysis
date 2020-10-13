import tweepy
from textblob import TextBlob
import preprocessor as p
import matplotlib.pyplot as plt

'''
print("Enter your consumer key")
consumer_key = input()
print("\nEnter your consumer secret ")
consumer_secret = input()
print("\nEnter your access token")
access_token = input()
print("\nEnter your access token secret")
access_token_secret = input()
'''
consumer_key ="Rd2Luk2JoqvDYAOT6PA5EAkG2"
consumer_secret="4mkt1YBGZSCBA0Doy4ZKdKpDlcwRS7hmzLpv7Besxl3Zw71nNU"
access_token="945831943052120065-n0TBgYL3oMwwr6wScvAVOoyWSWXIc7u"
access_token_secret="RSWdsnj0OeSqVkiaJCOcMeef1nBnb3dL9o90VWGGJro3i"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#initialize Tweepy API
api = tweepy.API(auth)

keyword=input("Enter a hashtag : ")
nbTweet = int(input("\nEnter how many tweets to search: "))
def get_tweets(keyword: str):
    
    all_tweets = []
    for tweet in tweepy.Cursor(api.search,q=keyword , tweet_mode="extended" , lang="en").items(nbTweet):
        all_tweets.append(tweet.full_text)

    return all_tweets

def clean_tweets(all_tweets):
    tweets_clean=[]
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))
    return tweets_clean

def get_sentiment():
    #Getting the clean tweets
    tweets = get_tweets(keyword)
    all_tweets= clean_tweets(tweets)
    
    #Creating some variables to store info
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    
    # iterating through tweets fetched
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        polarity += blob.sentiment.polarity  # adding up polarities to find the average later

        if (blob.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (blob.sentiment.polarity > 0 and blob.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (blob.sentiment.polarity > 0.3 and blob.sentiment.polarity <= 0.6):
            positive += 1
        elif (blob.sentiment.polarity > 0.6 and blob.sentiment.polarity <= 1):
            spositive += 1
        elif (blob.sentiment.polarity > -0.3 and blob.sentiment.polarity <= 0):
            wnegative += 1
        elif (blob.sentiment.polarity > -0.6 and blob.sentiment.polarity <= -0.3):
            negative += 1
        elif (blob.sentiment.polarity > -1 and blob.sentiment.polarity <= -0.6):
            snegative += 1
    
    # finding average of how people are reacting
    positive = percentage(positive, nbTweet)
    wpositive = percentage(wpositive, nbTweet)
    spositive = percentage(spositive, nbTweet)
    negative = percentage(negative, nbTweet)
    wnegative = percentage(wnegative, nbTweet)
    snegative = percentage(snegative, nbTweet)
    neutral = percentage(neutral, nbTweet)
    
    # finding average reaction
    polarity = polarity / nbTweet
    
    


    


    #printing the average reaction
    print("General Result: ")
    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")
        
     #printing the pourcentage of each reaction        
    print()
    print("Details: ")
    print(str(positive) + "%  of tweets are positives")
    print(str(wpositive) + "% of tweets are weakly positives")
    print(str(spositive) + "% of tweets are strongly positives")
    print(str(negative) + "% of tweets are negatives")
    print(str(wnegative) + "% of tweets are negatives")
    print(str(snegative) + "% of tweets are strongly negatives")
    print(str(neutral) + "% of tweets are neutrals")
    print()
    
    plotPie(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, nbTweet)

    
#calculating the pourcentage
def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

#visualizing the results in a Pie plot
def plotPie(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, nbTweet):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Analyzing ' + str(nbTweet) + ' tweets contaiting the word  ' + keyword)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__=="__main__":
    
    get_sentiment()
        