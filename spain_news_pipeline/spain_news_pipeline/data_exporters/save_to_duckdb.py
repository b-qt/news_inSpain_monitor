if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import duckdb
import pandas as pd

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to local duckdb database file

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # 1. Connect to file
    conn = duckdb.connect("news_db.duckdb")

    #2. Create table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            title TEXT, 
            published_date TIMESTAMP, 
            summary TEXT, 
            source_name TEXT, 
            source_url TEXT, 
            entry_date DATETIME, 
            title_english TEXT, 
            sentiment_label_en TEXT, 
            sentiment_score_en FLOAT, 
            sentiment_label_es TEXT, 
            sentiment_score_es FLOAT
        );
    """)

    conn.execute("CREATE TEMP TABLE new_batch AS SELECT * FROM data")
    conn.execute("""
        INSERT INTO news
        SELECT * FROM new_batch
        WHERE source_url NOT IN (SELECT source_url FROM news)
    """)

    conn.close()