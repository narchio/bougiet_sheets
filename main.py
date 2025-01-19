
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

def get_cleaned_df(df: pd.DataFrame): 
     # Step 2b: Clean the data and populate the new dataframe.
    cleaned_rows = []
    for index, row in df.iterrows(): 
        amex_row = AmericanExpressRow.clean_data(row)
        cleaned_rows.append(amex_row.convert_to_list())

    return pd.DataFrame(cleaned_rows, columns=COLUMNS)

def process(df: pd.DataFrame, existing_sheet_df: pd.DataFrame): 
    # Step 2: Clean data 
    # TODO(ncarchio): Step 2a: figure out what class to call (use the headers to figure it out 
    # -- each bank/credit card has its own headers)
    #           Note: can prob make all of these accounts an abstract class. Will make this code much simpler.

    # Step 2b: Clean the data and populate the new dataframe.
    new_df = get_cleaned_df(df)
    print(f"cleaned new df: {new_df}\n\n")


    # Keep track of the original length of existing entries from the db.
    db_entries_length = len(existing_sheet_df)
    # Combine the dataframes. 
    # Note: Currenty not using concat since we don't want the extra fully memory copy. However, we can optimize this in the future.
    for index, row in new_df.iterrows(): 
        current_index = db_entries_length + index
        existing_sheet_df.loc[current_index] = row
    print(f"Combined dfs{existing_sheet_df}, len: {len(existing_sheet_df)}")
    
    # Dedupe the dataframes to remove any entries that already exist.
    df_deduped = existing_sheet_df.drop_duplicates(subset='id', keep='first') 
    print(f"deduped: {df_deduped}, len: {len(df_deduped)}")


    # Now, get all new entries after deduping. 
    number_of_deduped_entries = (len(new_df) + db_entries_length) - len(df_deduped)
    number_of_new_entries = len(new_df) - number_of_deduped_entries
    start_index = len(df_deduped) - number_of_new_entries
    new_entries = []
    for index, row in df_deduped.iloc[start_index:].iterrows(): 
        new_entries.append(row)
    new_entries_df = pd.DataFrame(new_entries, columns=COLUMNS)
    print(f"new_entries_df {new_entries_df}")

    # Write the new entreis to google sheets. 
    # TODO(ncarchio): implement this

        







    

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
            existing_sheet_df =  get_cleaned_df(pd.read_csv(file_path))
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