from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional


class ContractCreate(BaseModel):
    number: str
    date: date
    city: str = "г. Новосибирск"

    customer_id: int

    contractor_keycloak_id: str
    contractor_full_name: str
    contractor_inn: str
    contractor_ogrn: str
    contractor_is_individual: bool = True
    contractor_legal_address: str
    contractor_bank_name: str
    contractor_bik: str
    contractor_account: str
    contractor_corr_account: str

    object_full_name: str
    object_address: Optional[str] = None

    basis_enabled: bool = False
    basis_type: Optional[str] = None
    basis_number: Optional[str] = None
    basis_date: Optional[date] = None

    date_start: date
    date_end: date

    amount: Decimal
    vat_included: bool = False

    tranch1_pct: int = 30
    tranch1_condition: str
    tranch2_pct: Optional[int] = None
    tranch2_condition: Optional[str] = None
    tranch3_pct: Optional[int] = None
    tranch3_condition: Optional[str] = None

    extra_conditions: Optional[str] = None
    works_text: str