import pandas as pd
import re
import datetime
from datetime import datetime, timedelta
import numpy as np

file = "anders.csv"

def filter_csv_file(file):
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        if pd.isna(row[0]) and pd.isna(row["3"]):
            df.drop(index, inplace=True)  # Remove row with NaN value in first column
        elif "Korrigerad av" in str(row["3"]):
            df.drop(index, inplace=True)  # Remove row with NaN value in first column
    df.reset_index(drop=True, inplace=True)

    for index, row in df.iterrows():
        if pd.isna(row["0"]) and len(str(row["3"])) < 6:
            df.drop(index, inplace=True)  # Remove row with NaN value in first column
    df.drop(0,inplace=True)
    new_df = pd.DataFrame({"Datum": df["0"], "Arbetad tid": df["3"]}).reset_index() # Removes the "Index" column when creating a new Data Frame and make order right numerical
    new_df = new_df.drop(columns=['index'])


    for index,row in new_df.iterrows():
        if " -" in str(row["Datum"]):
            new_df.drop(index, inplace=True)
        else:
            time_str = str(row["Arbetad tid"])
            if "Nästa dag" in time_str:
                time_str = time_str.rsplit(" (Nästa dag)")[0]
            new_df.loc[index, "Arbetad tid"] = time_str
    new_df.reset_index(drop=True, inplace=True)
    try:
        for index,row in new_df.iterrows():
            if pd.isna(row["Arbetad tid"]) or "min" in row["Arbetad tid"] or "nan" in (row["Arbetad tid"]):
                new_df.at[index, "Arbetad tid"] = new_df.at[index + 1, "Arbetad tid"]
    except Exception:
        pass

    for index,row in new_df.iterrows():
        try:
            if pd.isna(row["Datum"]) and pd.isna(new_df.at[index+1, "Datum"]):
                new_df.at[index+1, "Datum"] = new_df.at[index-1, "Datum"]
        except Exception:
            continue


    last_date = pd.Timestamp('1900-01-01')
    counter = 0
    for i, row in new_df.iterrows():
        if pd.isna(row['Arbetad tid']):
            counter += 1
        else:
            if counter >= 3:
                new_df.loc[i - counter:i - 1, 'Datum'] = last_date
            counter = 0
            last_date = row['Datum']
    new_df['Datum'].fillna(method='ffill', inplace=True)


    new_df = new_df.drop_duplicates()
    date_counts = new_df["Datum"].value_counts()
    time_counts = new_df["Arbetad tid"].value_counts()

    remove_dict = {}
    for date in new_df["Datum"].unique():
        if date_counts[date] > 2:
            remove_dict[str(date)] = []
            for time, count1 in time_counts.items():
                if count1 > 1:
                    remove_dict[str(date)].append(time)

    for index,row in new_df.iterrows():
        try:
            if str(row["Datum"]) in remove_dict.keys():
                for items in remove_dict.values():
                    if str(row["Arbetad tid"]) in items:
                        new_df.drop(index, inplace=True)
                    elif str(row["Arbetad tid"][-5:-3]) in items:
                        new_df.drop(index, inplace=True)
        except Exception:
            continue
    new_df.reset_index(drop=True, inplace=True)


    pattern = r'^\d{2}:\d{2} - \d{2}:\d{2}$'
    mask = new_df['Arbetad tid'].apply(lambda x: bool(re.match(pattern, str(x))))
    new_df = new_df.loc[mask]

    return new_df.reset_index().drop(columns=['index'])


def add_ob(df):
    OB_list = []
    for index, row in df.iterrows():
        d = pd.Timestamp(row["Datum"])
        FMT = '%H:%M'
        weekday = [0,1,2,3,4]
        end_of_shift = row["Arbetad tid"][-5:]
        start_of_shift = row["Arbetad tid"][:5]
        if int(end_of_shift[:2]) < int(start_of_shift[:2]):
            end_hour = str(int(end_of_shift[:2]) + 24).zfill(2)  # add 24 to hour component and pad with leading zeros
            end_of_shift = end_hour + end_of_shift[2:]
            OB_list.append((int(end_of_shift[:2])-int(start_of_shift[:2])))
            continue
        if d.dayofweek in weekday:
            if datetime.strptime(end_of_shift,FMT) >= datetime.strptime("20:00", FMT):
                OB = "20:00"
                ob_time = (datetime.strptime(end_of_shift, FMT) - datetime.strptime(OB, FMT))
                OB_list.append(ob_time.total_seconds()/60/60)
            else:
                OB_list.append(0)
        elif d.dayofweek == 5:
            if datetime.strptime(end_of_shift, FMT) >= datetime.strptime("16:00", FMT):
                OB = "16:00"
                ob_time = (datetime.strptime(end_of_shift, FMT) - datetime.strptime(OB, FMT))
                OB_list.append(ob_time.total_seconds()/60/60)
            else:
                OB_list.append(0)
        else:
            ob_time = (datetime.strptime(end_of_shift, FMT) - datetime.strptime(start_of_shift, FMT))
            OB_list.append(ob_time.total_seconds()/60/60)
    df["OB"] = OB_list
    return df



if __name__ == "__main__":
    filtered_dataframe = filter_csv_file(file)
    print(add_ob(filtered_dataframe))

