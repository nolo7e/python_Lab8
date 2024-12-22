from pydantic import BaseModel


class TermBase(BaseModel):
    keyword: str
    description: str


class TermCreate(TermBase):
    pass


class TermUpdate(BaseModel):
    description: str


class Term(TermBase):
    id: int

    class Config:
        from_attributes = True
