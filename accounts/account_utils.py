from datetime import datetime

def get_date_string(date_object: datetime): 
    return date_object.strftime("%m/%d/%Y")

def standardize_date(date_string):
    """
    Converts a date string in various formats to "m/dd/yyyy".

    Args:
        date_string: The date string to convert.

    Returns:
        A date string in "m/dd/yyyy" format, or None if the input is invalid.
    """
    formats_to_try = [
        "%m/%d/%Y",  # mm/dd/yyyy
        "%m/%d/%y",  # mm/dd/yy
        "%m-%d-%Y",  # mm-dd-yyyy
        "%m-%d-%y",  # mm-dd-yy
        "%d/%m/%Y",  # dd/mm/yyyy
        "%d/%m/%y",  # dd/mm/yy
        "%d-%m-%Y",  # dd-mm-yyyy
        "%d-%m-%y",  # dd-mm-yy
        "%Y/%m/%d",  # yyyy/mm/dd
        "%Y-%m-%d",  # yyyy-mm-dd
        "%m/%d/%Y %H:%M:%S", # mm/dd/yyyy hh:mm:ss
        "%m/%d/%y %H:%M:%S", # mm/dd/yy hh:mm:ss
        "%Y-%m-%d %H:%M:%S", # yyyy-mm-dd hh:mm:ss
        "%Y-%m-%dT%H:%M:%S", # ISO 8601 format
        "%Y-%m-%dT%H:%M:%SZ" # ISO 8601 format with Z
    ]

    for format in formats_to_try:
        try:
            return datetime.strptime(date_string, format)            
        except ValueError:
            # Try the next format, don't throw an error.
            pass  

    # No matching format found
    return None  

def clean_description(description: str): 
    """
    Returns a cleaned description string by removing all non alpha-numeric 
    characters with underscores. 

    Args:
        description: Raw description string from the csv file. 

    Returns:
        A cleaned string that replaces all non-alpha-numeric chars with underscores. 
    """
    result = ''
    for char in description: 
        if char.isalnum(): 
            result += char
        else: 
            result += '_'
    return result
        
    

def get_amount(amount: str): 
    """
    Returns the converted amount string into a float.

    Args: 
        amount: Raw amount string from the csv.
    
    Returns: 
        A amount float, assuming it parses and is in reasonable bounds. 
    """
    try: 
        float_amount = float(amount)
        if (float_amount > -100000 or float_amount < 100000): 
            return float_amount
        else: 
            raise ValueError("The float is out of reasonable bounds, something must have gone wrong.")
    except: 
        raise ValueError(f"The amount failed to parse. Amount: {amount}")


def create_id(date: datetime, description: str, amount: float): 
    return f'{get_date_string(date)}_{description}_{amount}'
