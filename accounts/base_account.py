from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel

class BaseAccount(BaseModel): 
    id: str
    date: datetime
    description: str
    amount: float
    category: str

    @abstractmethod
    def clean_data(cls, row: list) -> "BaseAccount | None":
        """
        This is an abstract method that must be implemented by subclasses.
        Subclasses must define how to clean and process the input data.
        """
        raise NotImplementedError
    
    def convert_to_list(self): 
        """
        Returns any instace of the BaseAccount as a list that can later be 
        used to populate a pd.Dataframe. 
        """
        return [
            self.id, 
            self.date, 
            self.description, 
            self.amount, 
            self.category
        ]