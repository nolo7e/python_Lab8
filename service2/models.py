from sqlmodel import SQLModel, Field


class Term(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    keyword: str = Field(index=True, nullable=False)
    description: str = Field(nullable=False)
