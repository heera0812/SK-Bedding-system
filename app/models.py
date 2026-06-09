from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Visitor:
    issue_id: str
    full_name: str
    mobile: str
    stay_days: int
    gadda_qty: int
    rajai_qty: int
    deposit_amount: int
    issue_datetime: datetime
    return_datetime: Optional[datetime]
    status: str

    @property
    def is_active(self) -> bool:
        return self.status == "active"


@dataclass
class Inventory:
    total_gadda: int
    available_gadda: int
    total_rajai: int
    available_rajai: int
    deposit_per_item: int
