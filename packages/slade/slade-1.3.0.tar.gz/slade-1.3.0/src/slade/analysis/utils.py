import pandas as pd

def raw_data_to_df(results):
    rows = []
    for result in results:
        metric = result.get('metric', {})
        values = result.get('values', [])

        for value in values:
            timestamp, val = value
            row = {
                'timestamp': pd.to_datetime(int(timestamp), unit='s'),  # Convert UNIX timestamp to datetime
                'value': float(val)
            }
            # Add metric labels to the row
            row.update(metric)
            rows.append(row)

        # Create a DataFrame from the rows
    df = pd.DataFrame(rows)
    return df