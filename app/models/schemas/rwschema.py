from app.models.domain.rwmodel import HoloModel


class RWSchema(HoloModel):
    class Config(HoloModel.Config):
        orm_mode = True
