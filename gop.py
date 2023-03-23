import pandas as pd
# Load data from CSV files
df1 = pd.read_csv('merged_all_local.csv')
df2 = pd.read_csv('merged_all.csv')
# df3 = pd.read_csv('all_item_diengiadung_301_600.csv')
# df4 = pd.read_csv('all_item_diengiadung_600_850.csv')
# Concatenate dataframes vertically
df_concat = pd.concat([df1, df2])
df_concat = df_concat.reset_index(drop=True)
df_concat.index += 1


# Save concatenated dataframe to a new CSV file
# df_concat = df_concat.drop('Unnamed: 0', axis=1)

df_concat.to_csv('merged_all_in.csv', index_label='id')
