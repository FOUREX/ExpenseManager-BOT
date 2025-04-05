from typing import Sequence
from datetime import datetime

from aiohttp import ClientSession

from src.expense_manager.types import Expense
from src.config import config


class ExpenseManagerClient:
    def __init__(self, base_url: str = config.API_URL):
        self.base_url = base_url

    async def get_expense(self, id: int) -> Expense | None:
        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/expense/{id}") as response:
                response_data = await response.json()

        if response_data is None:
            return None

        return Expense(**response_data)

    async def get_expenses(
            self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> Sequence[Expense]:
        params = {}
        params |= {"start_date": str(start_date)} if start_date is not None else {}
        params |= {"end_date": str(end_date)} if end_date is not None else {}

        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/expenses", params=params) as response:
                response_data = await response.json()

        return [Expense(**expense) for expense in response_data]

    async def create_expense(self, name: str, amount: float, created_at: datetime) -> Expense:
        payload = {
            "name": name[:128],
            "amount_uah": amount,
            "created_at": str(created_at)
        }

        async with ClientSession() as session:
            async with session.post(f"{self.base_url}/expense", json=payload) as response:
                response_data = await response.json()

        return Expense(**response_data)

    async def edit_expense(self, id: int, name: str, amount: float) -> Expense | None:
        payload = {
            "name": name[:128],
            "amount_uah": amount
        }

        async with ClientSession() as session:
            async with session.patch(f"{self.base_url}/expense/{id}", json=payload) as response:
                response_data = await response.json()

        if response_data is None:
            return None

        return Expense(**response_data)

    async def delete_expense(self, id: int) -> Expense | None:
        async with ClientSession() as session:
            async with session.delete(f"{self.base_url}/expense/{id}") as response:
                response_data = await response.json()

        if response_data is None:
            return None

        return Expense(**response_data)


expense_manager = ExpenseManagerClient()
