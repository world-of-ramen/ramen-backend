import logging

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "[DEV] World of Ramen application"

    description: str = "可用此token測試(wallet_address=0x1234567890):\n\n\
    Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjY0MTIzMzkzLCJzdWIiOiJhY2Nlc3MifQ.HULU9of8h9gz_oW6CzDxXvQxOvtE80PdOA-WRRwshcQ"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
