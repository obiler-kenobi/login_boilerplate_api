from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "8aff20dc5d697a58bec3cf507be78976946ecbfefae32cd9d2eb3b89e7e0d314"
    authjwt_algorith: str = "HS256"
    authjwt_access_token_expires: int = 15
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 30

