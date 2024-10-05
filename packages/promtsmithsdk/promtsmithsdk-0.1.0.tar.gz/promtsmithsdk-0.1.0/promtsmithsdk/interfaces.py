from typing import TypedDict, Optional
from uuid import UUID


class PromptResponse(TypedDict):
    unique_key: str
    description: str
    uuid: UUID
    name: int
    percentage: float
    content: str
    llm_model_name: Optional[str]
