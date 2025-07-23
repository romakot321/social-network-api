from pydantic import BaseModel


class FotobudkaPartnerStatResponse(BaseModel):
    class Data(BaseModel):
        amount: int

    error: str | None = None
    message: str | None = None
    data: Data