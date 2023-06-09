from pydantic import BaseModel


class TokenResBody(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    resource: str
    refresh_token: str
    refresh_token_expires_in: int
    id_token: str
    nt_account: str
    email: str
