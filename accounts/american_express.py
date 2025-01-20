from datetime import datetime
from accounts.base_account import BaseAccount
from accounts.account_utils import standardize_date, clean_description, get_amount, create_id

class AmericanExpressRow(BaseAccount): 
    id: str = ""
    date: datetime = None
    description: str = ""
    amount: float = 0
    category: str = ""

    def clean_data(self, row: list) -> "AmericanExpressRow | None":
        """"
        Builds the AmericanExpressRow, cleaning any necessary data as needed. 
        
        American Express CSV example: 
            Date,       Description,    Card Member,    Account #,  Amount
            12/20/2024, Amazon,         JOHN SMITH,            1,     -21.10 --> Refund
            12/20/2024, Amazon,         JOHN SMITH,            1,     45.83 --> Charge

        """
        # Date
        date = standardize_date(date_string=row[0])

        # Description 
        description = clean_description(description=row[1])

        # Amount
        amount = get_amount(amount=row[4])

        # Get the transaction id after all the data has been cleaned. 
        id = create_id(date, description, amount)
        
        # Category is set to nothing by default. 
        return AmericanExpressRow(
            id = id,
            date = date, 
            description = description, 
            amount = amount, 
            category = ''
        ) 
