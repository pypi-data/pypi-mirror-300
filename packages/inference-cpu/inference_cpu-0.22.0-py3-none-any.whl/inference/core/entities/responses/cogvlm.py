from typing import Optional

from pydantic import BaseModel, Field


class CogVLMResponse(BaseModel):
    response: str = Field(description="Text generated by CogVLM")
    time: Optional[float] = Field(
        None,
        description="The time in seconds it took to produce the response including preprocessing",
    )
