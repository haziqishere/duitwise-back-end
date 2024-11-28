from enum import Enum

class TaxReliefCategory(str, Enum):
    ELECTRONICS = "Electronics and Smartphones"
    SPORTS = "Sports and Recreation"
    MEDICAL = "Medical and Healthcare"
    OTHER = "Other Expenses"

STORE_CATEGORY_MAPPING = {
    "MACHINES": TaxReliefCategory.ELECTRONICS,
    "APPLE": TaxReliefCategory.ELECTRONICS,
    # Add more mappings as needed
}

def get_store_category(store_name: str) -> str:
    """Map store name to tax relief category"""
    store_upper = store_name.upper()
    return STORE_CATEGORY_MAPPING.get(store_upper, TaxReliefCategory.OTHER)