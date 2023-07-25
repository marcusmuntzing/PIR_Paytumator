import pandas as pd
import re


file = "felix_juni_combined.csv"

def filter_csv_file(file):
    df = pd.read_csv(file)

    # Drop rows with NaN values in first column or "Korrigerad av" in third column
    df = df.dropna(subset=[df.columns[0]], axis=0)
    df = df[~df[df.columns[2]].str.contains("Korrigerad av")]

    # Drop rows with NaN values in first column and length of third column < 6
    df = df.dropna(subset=[df.columns[0], df.columns[2]], how='all')
    df = df[~((df[df.columns[2]].str.len() < 6) & df[df.columns[0]].isna())]

    # Extract relevant columns and remove unwanted rows
    new_df = pd.DataFrame({"Datum": df["0"], "Arbetad tid": df["3"]}).reset_index()
    new_df = new_df.drop(columns=['index'])
    new_df = new_df[~new_df[new_df.columns[0]].str.contains(" -")]

    # Fill NaN values in Arbetad tid column and fix missing dates
    new_df['Arbetad tid'] = new_df['Arbetad tid'].fillna(method='ffill')
    new_df['Datum'] = new_df['Datum'].fillna(method='ffill')
    new_df['Datum'] = new_df['Datum'].fillna(method='bfill')

    # Fill missing dates for consecutive rows with missing Arbetad tid values
    mask = new_df['Arbetad tid'].isna()
    new_df.loc[mask, 'Datum'] = new_df.loc[mask, 'Datum'].shift(-1)
    new_df = new_df.dropna(subset=['Arbetad tid'])

    # Remove rows with duplicate Arbetad tid values for the same date
    new_df = new_df.drop_duplicates(subset=['Datum', 'Arbetad tid'])

    # Filter out rows that don't match the pattern "hh:mm - hh:mm" in Arbetad tid column
    pattern = r'^\d{2}:\d{2} - \d{2}:\d{2}$'
    mask = new_df['Arbetad tid'].apply(lambda x: bool(re.match(pattern, str(x))))
    new_df = new_df.loc[mask]

    return new_df




if __name__ == "__main__":
   filtered_dataframe = filter_csv_file(file)
   print(filtered_dataframe)

