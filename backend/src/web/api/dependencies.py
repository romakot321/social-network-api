from typing import Annotated

from fastapi import Depends

from src.account.api.dependencies import get_account_uow
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.task.api.dependencies import get_task_uow
from src.task.application.interfaces.task_uow import ITaskUnitOfWork

AccountUoWDepend = Annotated[IAccountUnitOfWork, Depends(get_account_uow)]
TaskUoWDepend = Annotated[ITaskUnitOfWork, Depends(get_task_uow)]