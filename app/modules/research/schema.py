from pydantic import BaseModel, Field


class QueriesSchema(BaseModel):
    queries: list[str] = Field(description="List of queries to research")


class ResearchInput(BaseModel):
    product_description: str
