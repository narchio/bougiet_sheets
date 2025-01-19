
import pandas as pd
import os
from accounts import AmericanExpressRow

COLUMNS = [
    'id',
    'date',
    'description',
    'amount',
    'category',
]

def clean_rows(df: pd.DataFrame): 
     # Step 2b: Clean the data and populate the new dataframe.
    cleaned_rows = []
    for index, row in df.iterrows(): 
        amex_row = AmericanExpressRow.clean_data(row)
        cleaned_rows.append(amex_row.convert_to_list())

    return pd.DataFrame(cleaned_rows, columns=COLUMNS)

def process(df: pd.DataFrame, existing_sheet_df: pd.DataFrame): 
    # Step 2: Clean data 

    # Step 2a: figure out what class to call (use the headers to figure it out 
    # -- each bank/credit card has its own headers)


    # Step 2b: Clean the data and populate the new dataframe.
    new_df = clean_rows(df)

    print(f"cleaned new df: {new_df}\n\n")


    # Step 3: 
    # dedupe new df with old df
    # test code to ensure dedupinng works 
    # old_df = new_df.copy()
    # old_length = len(old_df)
    # old_df['id'] = new_df['id'].apply(lambda x: x+"_next")
    # dup_row = old_df.iloc[0]
    # print(f"dup row: {dup_row}")
    # old_df.loc[len(old_df)] = dup_row
    # print(old_df)


    # keep track of the original length of the old df
    existing_len = len(existing_sheet_df)
    print(f"existing_len: {existing_len}")
    # append the new df onto the existing df
    for index, row in new_df.iterrows(): 
        current_index = existing_len + index
        existing_sheet_df.loc[current_index] = row

    print(f"{existing_sheet_df}, len: {len(existing_sheet_df)}")
    # dedupe them 
    df_deduped = existing_sheet_df.drop_duplicates(subset='id', keep='first') 
    print(f"deduped: {df_deduped}, len: {len(df_deduped)}")


    # then, from the old index to the end of the length of the new df, those will be 'new' entries
    number_of_deduped_entries = (len(new_df) + existing_len) - len(df_deduped)
    number_of_new_entries = len(new_df) - number_of_deduped_entries
    print(f"new entries: [{number_of_new_entries}]")

    start_index = len(df_deduped) - number_of_new_entries
    print(f"start index: {start_index}")
    new_entries = []
    for index, row in df_deduped.iloc[start_index:].iterrows(): 
        new_entries.append(row)

    new_entries_df = pd.DataFrame(new_entries, columns=COLUMNS)
    print(f"new_entries_df {new_entries_df}")

        







    

def main(): 
    # Step 1: Input the file.
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the folder path for the CSVs
    test_csv_folder_path = os.path.join(current_dir, "test_csvs/") 

    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(test_csv_folder_path) if f.endswith('.csv')]

    # Loop through each CSV file
    i = 0
    existing_sheet_df = []
    for file in csv_files:
        file_path = os.path.join(test_csv_folder_path, file)
        print(f"processing {file_path}")
        
        if (i == 0): 
            existing_sheet_df =  clean_rows(pd.read_csv(file_path))
            i += 1
            continue

        df = pd.read_csv(file_path) 
        print(f"existing df: {existing_sheet_df}")
        print(f"new df: {df}")
        process(df, existing_sheet_df)

        # increment i
        i += 1

# run main
main()