from pydantic import BaseModel, Field
from enum import Enum

class LoanType(str, Enum):
    MORTGAGE = "MORTGAGE"
    CAR = "CAR"
    PERSONAL = "PERSONAL"

class CurrentData(BaseModel):
    total_income: float = Field(..., gt=0)
    total_commitment: float = Field(..., ge=0)

class LoanDetails(BaseModel):
    loan_type: LoanType
    loan_amount: float = Field(..., gt=0)
    duration_months: int = Field(..., gt=0)
    percentage: float = Field(..., ge=0, le=100)

class StressTestRequest(BaseModel):
    current_data: CurrentData
    loan_details: LoanDetails

class StressTestResponse(BaseModel):
    dsr: float
    additional_payment: float
    total_new_monthly: float

class ReceiptResponse(BaseModel):
    store_name: str
    date: str
    subtotal: float
    category: str