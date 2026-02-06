from pydantic import BaseModel, Field
from typing import Optional

# Topic Create
class TopicCreate(BaseModel):
    name: str = Field(..., max_length=150)
    description: Optional[str]

# Topic Response
class TopicResponse(BaseModel):
    topic_id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

# Course Topic Mapping
class CourseTopicMap(BaseModel):
    course_id: int
    topic_id: int
    sequence_order: Optional[int]