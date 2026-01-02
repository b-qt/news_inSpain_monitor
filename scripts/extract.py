#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import feedparser
from datetime import datetime

import argparse

import warnings
warnings.filterwarnings("ignore")



URL_1 = "https://news.google.com/rss/search?q=Espa%C3%B1a&hl=es&gl=ES&ceid=ES%3Aes"
URL_2 = "https://news.google.com/rss/search?q=Spain&hl=en-US&gl=US&ceid=US%3Aen"

# ----------------------- Extract the data from the url
def fetch_raw_data(url:str) -> list[dict]:
    """
    _summary_ : This function fetches raw data from the inputed url

    Args:
        url (string): _description_
    """    
    data = feedparser.parse(url)['entries']
    
    return data

# ------------------------ Parse the data into dataframes
def parse_data_into_dataframe(input_dict:dict) -> pd.DataFrame:
    """
    _summary_ : This function parses the input dictionary into dataframe objects

    Args:
        input_dict (dict): _description_

    Returns:
        pd.DataFrame: _description_
    """   
    processed_data = []
    
    for entry in input_dict:
        row = {
            'title' : entry['title'],
            'published_date' : pd.to_datetime(entry['published']),
            'summary' : entry['summary'],
            'source_name' : entry['source']['title'],
            'source_url' : entry['source']['href'],
            'entry_date' : pd.to_datetime(datetime.now())
        }
        processed_data.append(row)

    return pd.DataFrame(processed_data)

# ---------------------------------------------------------------------TESTS
def test_raw_data(output) -> None:
    assert len(output) > 0, "Empty output object" 
    assert isinstance(output, list), f"Output is not a list, {type(output)}"
    assert isinstance(output[0], dict), f"Output is not a dictionary, {type(output[0])}"
    
def test_parsing(output) -> None:
    assert isinstance(output, pd.DataFrame), f"output has not been parsed to dataframe. Output is a {type(output)}"
    assert len(output)> 0, f"no entries in output"

    
def main():
    args = parser.parse_args()
    url = args.url
    
    raw_output = fetch_raw_data(url)
    test_raw_data(raw_output)

    clean_data = parse_data_into_dataframe(raw_output)
    test_parsing(clean_data)


if __name__=='__main__':
    parser = argparse.ArgumentParser("Extract data from url")
    parser.add_argument("url", 
                        help="pull data from this url", 
                        type="str", 
                        default=URL_1)
    
    main(parser)
    