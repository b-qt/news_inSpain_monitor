import feedparser
import pandas as pd
from datetime import datetime

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Defined globally for easy access
URLS = [
    "https://news.google.com/rss/search?q=Espa%C3%B1a&hl=es&gl=ES&ceid=ES%3Aes",
    "https://news.google.com/rss/search?q=Spain&hl=en-US&gl=US&ceid=US%3Aen"
]

@data_loader
def fetch_raw_data(*args, **kwargs) -> list:
    """
    Fetches raw data from the Google News RSS feeds for Spain.
    """    
    all_entries = []
    
    for url in URLS:
        print(f"Fetching data from: {url}")
        feed = feedparser.parse(url)
        
        # Adding entries to our master list
        if feed.entries:
            all_entries.extend(feed.entries)
    
    print(f"Total entries fetched: {len(all_entries)} {type(all_entries)}")
    return {'entries':all_entries}


@test
def test_raw_data(output) -> None:

    data = output.get('entries')

    assert data is not None, "The output is None"
    assert len(data) > 0, "Empty output object" 
    assert isinstance(data, list), f"Output is not a list, it is {type(output)}"
    
    # Check if the first item is a dictionary-like object (feedparser uses AttrDict)
    assert isinstance(data[0], dict) or hasattr(data[0], 'keys'), "Items are not dicts"