if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test 

import pandas as pd
from datetime import datetime

@transformer
def transform(data, *args, **kwargs):
    """
    Convert the output from parent block into a dataframe object

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        data frame
    """
    processed_data = []
    if isinstance(data, list):
        all_entries = data
    elif isinstance(data, dict):
        all_entries = data['entries']
    else:
        all_entries = [data] + list(args)

    for entry in all_entries:
        if not isinstance(entry, dict):
            continue

        row = {
            'title':entry.get('title'),
            'published_date': pd.to_datetime(entry.get('published')),
            'summary': entry.get('summary'),
            'source_name': entry['source']['title'],
            'source_url': entry['source']['href'],
            'entry_date': pd.to_datetime(datetime.now())
        }
        processed_data.append(row)

    return pd.DataFrame(processed_data)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), f"output has not been parsed ... currently {type(output)}"
