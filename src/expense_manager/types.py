from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    id: int
    name: str
    amount_uah: str
    amount_usd: str
    created_at: str
