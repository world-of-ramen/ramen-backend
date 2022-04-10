from app.models.domain.ramenmodel import RamenModel


class RamenSchema(RamenModel):
    class Config(RamenModel.Config):
        orm_mode = True
