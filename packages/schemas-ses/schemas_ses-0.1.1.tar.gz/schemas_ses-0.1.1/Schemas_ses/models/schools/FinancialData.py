from typing_extensions import Optional

from Schemas.models.model import AnnexeModel


class FinancialData(AnnexeModel):
    previous_year_balance: Optional[int]
    state_subsidy_amount: Optional[int]
    other_parent_contributions: Optional[int]
    other_financial_resources: Optional[int]