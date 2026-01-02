from mage_ai.data_preparation.variable_manager import get_variable
from sqlalchemy import create_engine
import pandas as pd 

# Retrieve the dataframe from your AI sentiment block
df = get_variable('spain_news_pipeline', 'convert_the__title__into_english_from_spanish', 'output_0')

# Create the engine
engine = create_engine('sqlite:///')

# Get the SQL schema
create_table_sql = pd.io.sql.get_schema(df, 'spain_news_monitor', con=engine)

print(f"""
---- DATA SCHEMA ---- 
{create_table_sql}
""")