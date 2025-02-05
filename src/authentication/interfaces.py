from pydantic import BaseModel

class LoginRequest(BaseModel):
    """
    It represents the input of the /save-user, /make-login and /make-register API
    """
    username: str
    password: str