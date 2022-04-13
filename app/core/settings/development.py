import logging

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "[DEV] World of Ramen application"

    description: str = (
        "可用此token測試:\n\n"
        + "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        + ".eyJpZCI6Miwid2FsbGV0X2FkZHJlc3MiOiIweGExMkQ5NTdDM0VENGEwMjc2YjljZEVkNzQyMjViY2Q2NGM0MTcx"
        + "MkQiLCJleHAiOjE2NjQzODE0NDcsInN1YiI6ImFjY2VzcyJ9.j2Nm0tQvKwnwZQTi7TbwTar5Sty1k6R0_HOtb0WwVKI"
    )

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
