from pydantic import BaseModel


class FotobudkaPartnerStatResponse(BaseModel):
    class Data(BaseModel):
        amount: int

    error: bool | None = None
    message: str | None = None
    data: Data
