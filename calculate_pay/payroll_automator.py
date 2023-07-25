from create_csv.pdf_to_csv import read_pdf_to_csv
from read_csv.test_translate import filter_csv_file, add_ob
import os
import pandas as pd
import csv
import datetime


def sum_all_files(month):
    pdf_directory = fr"C:\Users\marcu\pay_automator\pdf_files\{month}"
    csv_directory = fr"C:\Users\marcu\pay_automator\csv_files\{month}"

    for filename in os.listdir(pdf_directory):
        f = os.path.join(pdf_directory, filename)
        if os.path.isfile(f):
            name_string = f.rsplit("\\")
            read_pdf_to_csv(f,csv_directory, f"{name_string[-1][:-4]}")

    name_list = []
    ob_sum_list = []
    total_hours_worked_list = []
    number_of_times_worked = []
    for filename in os.listdir(csv_directory):
        f = os.path.join(csv_directory, filename)
        if os.path.isfile(f):
            name = f.rsplit("\\")[-1].rsplit("_"+month)
            filtered_csv = filter_csv_file(f)
            ob_df = add_ob(filtered_csv)
            name_list.append(name[0])
            ob_sum_list.append(ob_df["OB"].sum())
            FMT = '%H:%M'
            sum_hours = 0
            for index,row in ob_df.iterrows():
                end_of_shift = row["Arbetad tid"][-5:]
                start_of_shift = row["Arbetad tid"][:5]
                if datetime.datetime.strptime(end_of_shift, FMT).time() >= datetime.time(0):
                    end_hours = pd.to_timedelta(end_of_shift + ':00').total_seconds() / 3600
                    start_hours = pd.to_timedelta(start_of_shift + ':00').total_seconds() / 3600
                    time_diff = (end_hours + 24 - start_hours) % 24
                    sum_hours += (time_diff)
                else:
                    total_time = (datetime.strptime(end_of_shift, FMT) - datetime.strptime(start_of_shift, FMT))
                    sum_hours += (total_time.total_seconds()/60/60)
            total_hours_worked_list.append(sum_hours)
            number_of_times_worked.append(ob_df["Datum"].nunique())
            sum_hours = 0
    return name_list, total_hours_worked_list,number_of_times_worked, ob_sum_list



def summary_dataframe(names,hour,num_times, obs):
    hours = [round(hour*2)/2 for hour in hour]
    ob = [round(ob*2)/2 for ob in obs]
    list_of_tuples = list(zip(names,hours,num_times, ob))
    df = pd.DataFrame(list_of_tuples, columns=["Namn", "Arbetade timmar", "Antal Pass", "Total OB"])
    return df



def export_summary_to_csv(summary_df, month):
    dir_name = fr"C:\Users\marcu\pay_automator\month_summaries"
    summary_df.to_csv(f"{dir_name}\{month}.csv")






if __name__ == "__main__":
    month = "juni"
    names, hours, num_times_work, ob = sum_all_files(month)
    summary_df = summary_dataframe(names,hours, num_times_work, ob)
    export_summary_to_csv(summary_df, month)
