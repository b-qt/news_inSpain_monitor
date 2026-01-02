if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import torch 
from transformers import pipeline
 
@transformer
def transform(data, *args, **kwargs):
    assert isinstance(data, pd.DataFrame), "data is not a dataframe!!"
    
    # 1. FIX: Use the correct model for TRANSLATION
    print("Loading translation model (Helsinki-NLP ES -> EN)...")
    pipeline_translation = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")

    # 2. Loading the Sentiment Analyzers
    print("Loading English sentiment analyzer (DistilBERT)...")
    pipeline_sentiment_en = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    
    print("Loading Spanish sentiment analyzer (Robertuito)...")
    pipeline_sentiment_es = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")

    # Clean titles (Removing source after the hyphen)
    titles_es = data['title'].str.rsplit("-", n=1).str[0].str.strip().to_list()

    # TRANSLATION
    print(f"Translating {len(titles_es)} items...")
    translations = pipeline_translation(titles_es, truncation=True)
    # Helsinki-NLP returns a list of dicts with 'translation_text'
    data['title_english'] = [t['translation_text'] for t in translations]

    # SENTIMENT ANALYSIS
    print("Analyzing sentiment (English and Spanish)...")
    
    # Run English sentiment on translated titles
    sent_en_results = pipeline_sentiment_en(data["title_english"].to_list(), truncation=True)
    
    # Run Spanish sentiment on original (cleaned) titles
    sent_es_results = pipeline_sentiment_es(titles_es, truncation=True)
    
    # Map results for English model
    data['sentiment_label_en'] = [s['label'] for s in sent_en_results]
    data['sentiment_score_en'] = [s['score'] for s in sent_en_results] 

    # Map results for Spanish model (Robertuito)
    label_map = {'POS': 'Positive', 'NEU': 'Neutral', 'NEG': 'Negative'}
    data['sentiment_label_es'] = [label_map.get(s['label'], s['label']) for s in sent_es_results]
    data['sentiment_score_es'] = [s['score'] for s in sent_es_results]

    return data

@test
def test_output(output, *args) -> None:
    assert 'title_english' in output.columns, 'Translation column missing'
    assert 'sentiment_label_es' in output.columns, 'Spanish Sentiment column missing'