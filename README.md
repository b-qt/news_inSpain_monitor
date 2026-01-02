# Pulse on the Iberian Region: Spanish newsletter monitor

I'm building a fully automated pipeline that scrapes Spanish-language news headlines about Spain, translates them into English using AI, assesses the "sentiment" (Positive/Negative) of the news, and stores them for analysis.  
__Serverless__ ... Instead of running a dedicated database server, I'm using a serverless data warehouse -_DuckDB_ for storage and _HuggingFace Inference API_ for the heavylifting. This is going to be orchestrated by _Mage_ running in _Docker_.  

## The Stack
- Orchestration -> Mage in Docker
- Compute/Transformations -> Python|pandas
- ML & Transformations -> Serverless HuggingFace Inference API
- Storage -> DuckDB
- Visualization | Frontend -> Looker Studio and/or streamlit

## Data source 
> _google news rss feeds_   
[Link 1](https://news.google.com/rss/search?q=Espa%C3%B1a&hl=es&gl=ES&ceid=ES%3Aes) ;  
[Link 2](https://news.google.com/rss/search?q=Spain&hl=en-US&gl=US&ceid=US%3Aen)

__Why__? free, realtime, legal to scrape via rss and allows complex filtering.  


## Machine learning component
Using models from huggingface ...  
- Translation (Spanish-to-English) | helsinki-nlp
- Sentiment Analysis | distilbert

### What is exciting about this project?
Other tha guaging the mood of the country via the news outlets ???  
- The prospect of batching when using the huggingface api
- RSS feed date formats
- Possibility of duplicate data so i need to implement data quality checks.
- Working with realtime data from API calls.
- _Enriching_ the data with AI.
- Offloading sstorage and compute to the cloud, hence keeping my docker container lightweight.