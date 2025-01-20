import pandas as pd
from colorama import Fore, Style
from accounts.american_express import AmericanExpressRow
from constants import CATEGORIES, COLUMNS

# -------------------
# Data cleaning functions 
# -------------------

# Clean the data and populate the new dataframe.
def get_cleaned_df(df: pd.DataFrame): 
    cleaned_rows = []
    for index, row in df.iterrows(): 
        amex_row = AmericanExpressRow().clean_data(row)
        cleaned_rows.append(amex_row.convert_to_list())

    return pd.DataFrame(cleaned_rows, columns=COLUMNS)

# -------------------
# Category functions 
# -------------------
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