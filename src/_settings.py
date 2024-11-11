from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AGRILLA_API_KEY: str
    AGRILLA_API_URL: str
    HF_TOKEN: str


_settings = Settings(_env_file=".env")

if __name__ == "__main__":
    print(_settings)
