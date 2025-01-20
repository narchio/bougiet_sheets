
import pandas as pd
import os

from accounts.account_utils import get_date_string
from budgeting_logic.logic import categorize_rows, get_cleaned_df
from budgeting_logic.constants import COLUMNS
from budgeting_logic.google_sheets import get_worksheet, get_existing_transactions

def process_file(df: pd.DataFrame, existing_sheet_df: pd.DataFrame): 
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


    # Get all new entries after deduping. 
    number_of_deduped_entries = (len(new_df) + db_entries_length) - len(df_deduped)
    number_of_new_entries = len(new_df) - number_of_deduped_entries
    start_index = len(df_deduped) - number_of_new_entries
    new_entries = []
    for index, row in df_deduped.iloc[start_index:].iterrows(): 
        new_entries.append(row)
    new_entries_df = pd.DataFrame(new_entries, columns=COLUMNS)
    print(f"new_entries_df {new_entries_df}")

    # Convert dates to a list 
    new_entries_df['date'] = new_entries_df['date'].apply(lambda date: get_date_string(date))

    # Categorize all rows if they don't already have a category. 
    # TODO(ncarchio): 1. Try to 'auto' categorize based off of the Categories map
    #   - within this, we should be able to automatically categorize and if we find it is 
    #    an 'IGNORE', we remove that from the dataframe
    # 2. If we can't auto categorize, ask user for manual input. 
    new_entries_df = categorize_rows(new_entries_df)

    # Write the new entreis to google sheets. 
    finalized_new_transactions = new_entries_df.values.tolist()
    worksheet = get_worksheet()
    worksheet.append_rows(finalized_new_transactions)

    print("""
    -----------------------------------------------------------------------
    Thanks for using bougiet, now, head over to Google Sheets and enjoy :) 
    -----------------------------------------------------------------------
    """)



def main(): 
    # Step 1: Fetch the input files.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_csv_folder_path = os.path.join(current_dir, "test_csvs/") 
    csv_files = [f for f in os.listdir(test_csv_folder_path) if f.endswith('.csv')]

    # Step 2: Get all the transactions from sheets. 
    existing_sheet_df = get_existing_transactions()
    
    # Step 3: Loop through each CSV file.
    for file in csv_files:
        file_path = os.path.join(test_csv_folder_path, file)
        print(f"processing {file_path}")

        df = pd.read_csv(file_path) 
        print(f"existing df: {existing_sheet_df}")
        print(f"new df: {df}")

        process_file(df, existing_sheet_df)
        
# Run the main function
main()


