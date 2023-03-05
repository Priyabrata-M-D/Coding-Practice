#import json
import base64
import streamlit as st
from mongoconfi import upload_to_mongodb
from tscrape import scrape_twitter_data


# Define the Streamlit app
def main():
    # Page title
    st.title('Twitter Scraper')

    # Get user input
    hashtag = st.text_input('Hashtag/Keyword')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    max_tweets = st.number_input('Max Tweets')

    # Scrape Twitter data
    if st.button('Scrape'):
        tweets_df = scrape_twitter_data(hashtag, start_date, end_date, max_tweets)

        # Create JSON file
        json_file = 'tweets.json'
        tweets_df.to_json(json_file, orient='records')

        # Display data in a table
        st.write(tweets_df)

        # Download data in CSV format
        csv = tweets_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown('### Download CSV File')
        href = f'<a href="data:file/csv;base64,{b64}" download="twitter_data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Download data in JSON format
        json = tweets_df.to_json(orient='records')
        b64 = base64.b64encode(json.encode()).decode()
        st.markdown('### Download JSON File')
        href = f'<a href="data:file/json;base64,{b64}" download="twitter_data.json">Download JSON</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Upload data to MongoDB
        if st.button('Upload to MongoDB'):
            result = upload_to_mongodb(json_file)
            # Display result
            st.write(f'{len(result.inserted_ids)} documents uploaded to MongoDB')

if __name__ == '__main__':
    main()



from pymongo import MongoClient
import json


# Define a function to upload data to MongoDB
def upload_to_mongodb(json_file):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['twitter_scraping']
    collection = db['scrapped1']
    # Convert data to JSON records and Insert data into MongoDB
    #result = collection.insert_many(json.dumps(scrap.to_dict('records')))
    with open(json_file, 'r') as f:
        data = json.load(f)
    result = collection.insert_many(data)

    return result



"""import snscrape.modules.twitter as sntwitter
import pandas as pd


# Define a function to scrape Twitter data
def scrape_twitter_data(hashtag, start_date, end_date, max_tweets):
    tweets_list = []
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f'{hashtag} since:{start_date} until:{end_date}').get_items()):
        if i >= max_tweets:
            break
        tweets_list.append(
            [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.source, tweet.likeCount])
    tweets_df = pd.DataFrame(tweets_list,
                             columns=["Date", "ID", "URL", "Content", "User", "Reply Count", "Retweet Count",
                                      "Language",
                                      "Source", "Like Count"])
    return tweets_df
"""