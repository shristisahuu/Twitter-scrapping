# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:01:06 2023

@author: Shristi
"""

import streamlit as st
import snscrape.modules.twitter as sntwitter 
import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


db = myclient["twitter_db"]
col = db ["tweets"]

def scrape_tweets(keyword, start_date, end_date, limit):
    query = f"{keyword} since: {start_date} until {end_date}"
    tweet_list = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):

        if i >= limit:
            break
   
        tweet_dict = {"id": tweet.id, 
                   "date": tweet.date,
                   "content":tweet.content ,
                   "likes": tweet.likeCount,
                   "retweets": tweet.retweetCount,
                   "language": tweet.lang,
                   "source": tweet.source,
                   
                   }
        tweet_list.append(tweet_dict)

    col.insert_many(tweet_list)
    st.success(f"{len(tweet_list)} tweets saved to database")
    

def app ():
    st.title("Twitter Scrapper")
    
    keyword = st.text_input("Enter a keyword or hashtag to search")
    
    start_date=st.date_input("start date")
    end_date = st.date_input("end date")
    
    limit = st.number_input("maximum number of tweets to scrape:", 
                            min_value=(1))
    if st.button("scrape"):
        scrape_tweets(keyword, start_date, end_date, limit)
     
    tweet_data= pd.DataFrame(list(col.find()))
    
    csv_data = tweet_data.to_csv(index = False)
    st.download_button("Download CSV", data=csv_data, file_name=("tweet_data"))