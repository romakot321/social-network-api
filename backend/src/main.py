from fastapi import FastAPI

from src.core.logging_setup import setup_fastapi_logging
from src.db.engine import engine
from src.task.api.rest import router as task_router
from src.account.api.rest import router as account_router
from src.web.api.rest import router as web_router
from src.report.api.rest import router as report_router

app = FastAPI(title="Social Network API")
setup_fastapi_logging(app)

app.include_router(task_router, tags=["Task"], prefix="/api/task")
app.include_router(account_router, tags=["Account"], prefix="/api/account")
app.include_router(web_router, tags=["Web"])
app.include_router(report_router, tags=["Report"], prefix="/api/report")

from sqladmin import Admin
from src.core.admin import authentication_backend
from src.task.api.admin import TaskAdmin

admin = Admin(app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(TaskAdmin)
