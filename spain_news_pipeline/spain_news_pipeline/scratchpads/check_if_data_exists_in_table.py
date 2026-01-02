"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""

from mage_ai.data_preparation.variable_manager import get_variable
from sqlalchemy import create_engine
import pandas as pd


# 1. Get data
df = get_variable('spain_news_pipeline', 
                  'convert_the__title__into_english_from_spanish', 
                  'output_0')

#2. Create fresh connection engine
engine = create_engine('sqlite:///')

#3. create table and load the data
df.to_sql('spain_news_monitor',
          con = engine,
          index=False,
          if_exists='replace')

# run the query
query = """
    select 
        title,
        sentiment_label_en,
        sentiment_label_es,
        sentiment_score_en,
        sentiment_score_es
    from spain_news_monitor
    where sentiment_label_es = 'Negative'
    order by sentiment_score_en DESC
    limit 10
"""

# Execute and look at the results
resulting_df = pd.read_sql(query,
                           con=engine)

print(f"""
\t\t\t---- QUERY RESULTS ---- \n\n
{resulting_df}
""")