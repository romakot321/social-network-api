from src.core.http.client import AsyncHttpClient
from src.integration.infrastructure.task_runner import TaskRunner
from src.task.application.interfaces.task_runner import ITaskRunner


def get_integration_task_runner() -> ITaskRunner:
    return TaskRunner()
