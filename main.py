
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from accounts.american_express import AmericanExpressRow
from accounts.account_utils import get_date_string
from colorama import Fore, Style

COLUMNS = [
    'id',
    'date',
    'description',
    'amount',
    'category',
]

CATEGORIES = {
        0: 'Restaurants',
        1: 'Groceries',
        2: 'Clothing', 
        3: 'Entertainment', 
        4: 'Gas', 
        5: 'Gifts', 
        6: 'Insurance',
        7: 'House Stuff', 
        8: 'Internet', 
        9: 'Luna Stuff', 
        10: 'Medical', 
        11: 'Other', 
        12: 'Parking', 
        13: 'Phone', 
        14: 'Rent/Mortgage', 
        15: 'Utilities', 
        16: 'Travel', 
        17: 'IGNORE', 
    }


def get_cleaned_df(df: pd.DataFrame): 
     # Step 2b: Clean the data and populate the new dataframe.
    cleaned_rows = []
    for index, row in df.iterrows(): 
        amex_row = AmericanExpressRow().clean_data(row)
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

    # Convert dates to a list 
    new_entries_df['date'] = new_entries_df['date'].apply(lambda date: get_date_string(date))

    # Categorize all rows if they don't already have a category. 
    # 1. Try to 'auto' categorize based off of the Categories map
    #   - within this, we should be able to automatically categorize and if we find it is 
    #    an 'IGNORE', we remove that from the dataframe
    # 2. If we can't auto categorize, ask user for manual input. 
    new_entries_df = categorize_rows(new_entries_df)

    # Write the new entreis to google sheets. 
    finalized_new_transactions = new_entries_df.values.tolist()
    worksheet = get_worksheet()
    worksheet.append_rows(finalized_new_transactions)

    
def get_worksheet(): 
    sheets = workbook.worksheets()
    print(sheets)
    return workbook.worksheet('Transactions')


def get_existing_transactions(): 
    raw_transactions = get_worksheet().get_all_values()
    return pd.DataFrame(raw_transactions[1:], columns=COLUMNS)


def get_category_input(description: str): 
    print(Fore.YELLOW + f"It's time to categorize all of your transactions. Please add your input below." + Style.RESET_ALL)
    print(Fore.GREEN + f"Enter the number of one of the following categories.\nCurrent transaction: {description}" + Style.RESET_ALL)
    for key, value in CATEGORIES.items(): 
        print(f"{key}: {value}")
    category_input = int(input(Fore.CYAN + f"\nCategory: " + Style.RESET_ALL))
    return category_input


def categorize_rows(df: pd.DataFrame):
    for index, row in df.iterrows(): 
        # Skip already categorized rows.
        if len(df.loc[index, 'category']) > 0: 
            continue
        category_input = get_category_input(row.description)
        df.loc[index,'category'] = CATEGORIES[category_input]

    print(f"df after: {df}")
    return df


def main(): 
    # Step 1: Input the file.
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the folder path for the CSVs
    test_csv_folder_path = os.path.join(current_dir, "test_csvs/") 

    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(test_csv_folder_path) if f.endswith('.csv')]

    # Get all the transactions from sheets. 
    existing_sheet_df = get_existing_transactions()
    
    # Loop through each CSV file
    for file in csv_files:
        file_path = os.path.join(test_csv_folder_path, file)
        print(f"processing {file_path}")

        df = pd.read_csv(file_path) 
        print(f"existing df: {existing_sheet_df}")
        print(f"new df: {df}")

        process(df, existing_sheet_df)
        
        


# run main
main()


