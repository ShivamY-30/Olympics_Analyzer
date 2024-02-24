import pandas as pd

def preprocessor(df ,region_df ):
    # Filter for summer
    df = df[df['Season'] == 'Summer']
    # Merge both
    df = df.merge(region_df, on='NOC', how='left')
    # remove duplicate
    df.drop_duplicates(inplace=True)
    # One hot encoding
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df


