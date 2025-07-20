from typing import Annotated

from fastapi import Depends

from src.account.application.account_adapter import AccountAdapter
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.infrastructure.db.account_uow import PGAccountUnitOfWork
from src.task.application.interfaces.task_account_adapter import ITaskAccountAdapter


def get_account_uow() -> IAccountUnitOfWork:
    return PGAccountUnitOfWork()


def get_account_adapter() -> ITaskAccountAdapter:
    return AccountAdapter(get_account_uow())


AccountUoWDepend = Annotated[IAccountUnitOfWork, Depends(get_account_uow)]