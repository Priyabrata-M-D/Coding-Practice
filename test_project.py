import pandas as pd
import snscrape.modules.twitter as sntwitter

# Get user input
hashtag = input("Enter the hashtag or keyword to search: ")
start_date = input("Enter the start date in YYYY-MM-DD format: ")
end_date = input("Enter the end date in YYYY-MM-DD format: ")
tweet_count = int(input("Enter the number of tweets to scrape: "))

# Create an empty list to store the scraped data
tweets_list = []

# Use sn-scrape to scrape the data and append it to the list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{hashtag} since:{start_date} until:{end_date}").get_items()):
    if i >= tweet_count:
        break
    tweets_list.append(
        [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
         tweet.lang, tweet.source, tweet.likeCount])

# Create a pandas dataframe from the list
tweets_df = pd.DataFrame(tweets_list,
                         columns=["Date", "ID", "URL", "Content", "User", "Reply Count", "Retweet Count", "Language",
                                  "Source", "Like Count"])

# Print the dataframe
print(tweets_df)





from pymongo import MongoClient


def upload_to_mongodb(data, tweets_df, scrapped):
    # Set up a connection to MongoDB
    client = MongoClient()

    # Select the database and collection
    db = client[tweets_df]
    collection = db[scrapped]

    # Insert the data into the collection
    collection.insert_many(data.to_dict('records'))



import streamlit as st
import pandas as pd
from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient("mongodb+srv://dsa830dsa:Priy%408908@cluster0.o5d3gwp.mongodb.net/test")
db = client[twitter_scraping]
collection = db[scrapped]


# Define function to scrape tweets and store in MongoDB
def scrape_tweets(keyword, start_date, end_date, tweet_count):
    # Use snscrape to scrape tweets
    tweets = pd.read_json(
        f"https://twitter.com/search?q={keyword}%20since%3A{start_date}%20until%3A{end_date}&src=typd&count={tweet_count}&lang=en")
    tweets["date"] = tweets["date"].apply(lambda x: str(x)[:10])

    # Convert tweets dataframe to a list of dictionaries
    tweet_list = tweets.to_dict("records")

    # Store the scraped tweets in MongoDB
    for tweet in tweet_list:
        collection.insert_one(tweet)


# Define function to download data in CSV format
def download_csv():
    cursor = collection.find()
    tweets = pd.DataFrame(list(cursor))
    tweets = tweets.drop(columns="_id")
    csv = tweets.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="tweets.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)


# Define function to download data in JSON format
def download_json():
    cursor = collection.find()
    tweets = pd.DataFrame(list(cursor))
    tweets = tweets.drop(columns="_id")
    json_data = tweets.to_json(orient="records")
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="tweets.json">Download JSON file</a>'
    st.markdown(href, unsafe_allow_html=True)


# Create the Streamlit app
def app():
    st.title("Twitter Scraper")

    # Get user input
    keyword = st.text_input("Enter a keyword or hashtag:")
    start_date = st.date_input("Start date:")
    end_date = st.date_input("End date:")
    tweet_count = st.slider("Number of tweets to scrape:", 1, 1000, 100)

    # Scrape tweets and store in MongoDB
    if st.button("Scrape tweets"):
        scrape_tweets(keyword, start_date, end_date, tweet_count)
        st.success("Tweets scraped successfully!")

    # Display scraped data in a table
    cursor = collection.find()
    tweets = pd.DataFrame(list(cursor))
    tweets = tweets.drop(columns="_id")
    st.write(tweets)

    # Download data in CSV or JSON format
    if st.button("Download CSV"):
        download_csv()
    if st.button("Download JSON"):
        download_json()