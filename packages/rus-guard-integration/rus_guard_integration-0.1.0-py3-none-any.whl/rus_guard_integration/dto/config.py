from pydantic import BaseModel


class RusGuardConfig(BaseModel):
    sever_ip: str
    rus_guard_login: str
    rus_guard_password: str