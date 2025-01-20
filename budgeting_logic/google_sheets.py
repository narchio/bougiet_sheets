import gspread
import pandas as pd

from google.oauth2.service_account import Credentials
from budgeting_logic.constants import COLUMNS
from settings import SETTINGS

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(info=SETTINGS['google_sheets_credentials'], scopes=scopes)
client = gspread.authorize(creds)

workbook_id = SETTINGS['workbook_id']
workbook = client.open_by_key(workbook_id)

def get_worksheet(): 
    sheets = workbook.worksheets()
    print(sheets)
    return workbook.worksheet('Transactions')

def get_existing_transactions(): 
    raw_transactions = get_worksheet().get_all_values()
    return pd.DataFrame(raw_transactions[1:], columns=COLUMNS)