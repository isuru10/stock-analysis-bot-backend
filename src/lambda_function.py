import os
from pathlib import Path
import tweepy
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'stock_market_chatbot'))
from technical_indicators_calculator import set_technical_indicators, Company
from technical_indicators_chart_plotting import TechnicalIndicatorsChartPlotter
import yfinance as yf

ROOT = Path(__file__).resolve().parents[0]

def lambda_handler(event, context):
    company_symbol = event['symbol']
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # print("Get tweet from csv file")
    # tweets_file = ROOT / "tweets.csv"
    # recent_tweets = api.user_timeline()[:3]
    # tweet = get_tweet(tweets_file)

    # print(f"Post tweet: {tweet}")
    # api.update_status(tweet)

    company = Company(company_symbol)
    config = {}
    company.prices = yf.Ticker(company.symbol).history(period='3mo')['Close']
    set_technical_indicators(config, company)

    tacp = TechnicalIndicatorsChartPlotter()
    tacp.plot_macd(company)
    tacp.plot_rsi(company)
    tacp.plot_bollinger_bands(company)

    ID = event['user_id']

    # upload media
    media_bb = api.media_upload(filename=f'/tmp/{company_symbol}_bb.png')
    media_macd = api.media_upload(filename=f'/tmp/{company_symbol}_macd.png')
    media_rsi = api.media_upload(filename=f'/tmp/{company_symbol}_rsi.png')

    api.send_direct_message(recipient_id=ID, text=f'Technical analysis for {company_symbol}')
    api.send_direct_message(recipient_id=ID, attachment_type='media', attachment_media_id=media_bb.media_id, text='')
    api.send_direct_message(recipient_id=ID, attachment_type='media', attachment_media_id=media_macd.media_id, text='')
    api.send_direct_message(recipient_id=ID, attachment_type='media', attachment_media_id=media_rsi.media_id, text='')

    return {"statusCode": 200, "tweet": company_symbol}
