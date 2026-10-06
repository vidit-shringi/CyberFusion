from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
class Settings(BaseSettings):
    app_name: str="CyberFusion"
    environment: str="development"
    database_url: str="sqlite:///./cyberfusion.db"
    secret_key: str="cyberfusion-dev-secret-please-change-32chars-min"
    jwt_secret: str="cyberfusion-dev-jwt-secret-please-change-32chars-min"
    access_token_expire_minutes: int=120
    incident_threshold: float=50.0
    frontend_origin: list[str]=["http://127.0.0.1:8000","http://localhost:8000","http://127.0.0.1:5500","http://localhost:5500"]
    nvd_api_key: str|None=None
    cisa_kev_url: str="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    admin_username: str="admin"
    admin_password: str="ChangeMe123!"
    model_config=SettingsConfigDict(env_file=".env",env_prefix="",extra="ignore")
    @field_validator("frontend_origin",mode="before")
    @classmethod
    def parse_origins(cls,v):
        if isinstance(v,str): return [x.strip() for x in v.split(",") if x.strip()]
        return v
settings=Settings()
