# import pandas as pd
#
#
# file = "felix_juni_combined.csv"
# df = pd.read_csv(file)
#
#
# for index, row in df.iterrows():
#     if pd.isna(row[0]) and pd.isna(row[4]):  # Check if value in first column is NaN
#         df.drop(index, inplace=True)  # Remove row with NaN value in first column
# df.drop(0,inplace=True)
# new_df = pd.DataFrame({"Datum": df["0"], "Arbetade timmar": df["4"]}).reset_index() # Removes the "Index" column when creating a new Data Frame and make order right numerical
# new_df = new_df.drop(columns=['index'])
#
#
# for index, row in new_df.iterrows():
#     try:
#         if "min" in row[1] and "h" not in row[1]:
#             new_df.loc[index - 1,"Arbetade timmar"] += " " + row[1]
#             new_df.drop(index, inplace=True)  # Remove row with NaN value in first column
#     except TypeError:
#         continue
#
#
#
# print(new_df)
#
# for index,row in new_df.iterrows():
#     if pd.isna(row[0]) or "/" in row[0]:  # Check if value in first column is NaN
#         new_df.drop(index, inplace=True)# Remove row with NaN value in first column
#     elif pd.isna(row[1]) and row[0] != None:
#         new_df.drop(index, inplace=True)# Remove row with NaN value in first column
#     elif " -" in row[0]:
#         new_df.drop(index, inplace=True) # Remove row with "-" value in date column
#
# new_df = new_df.reset_index().drop(columns=['index'])
#




#### REMOVING THE ODD NaN's WHEN ENCOUNTERED. WORKED FOR SOLVING LONG LINES OF NANS HOWEVER CHANGED THE VALUE OF OTHERS VALUES #####

# for i in range(1, len(df)):
#    try:
#        if pd.isna(new_df.at[i, "Datum"]) and pd.isna(new_df.at[i - 1, "Datum"]):
#            if i % 2 == 0:
#                new_df.drop(i, inplace=True)
#    except Exception:
#        pass