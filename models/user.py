from pydantic import BaseModel
from typing import Optional
from datetime import date

class User(BaseModel):
    id: Optional[int]
    full_name: str
    birth_date: date
    address: str
    profession: str
    phone: str      
    email: str
    father_name: str
    mother_name: str
    main_complaint: str
    father_age: Optional[str]
    mother_age: Optional[str]
