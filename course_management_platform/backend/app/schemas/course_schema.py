from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# University Schemas
class UniversityCreate(BaseModel):
    name: str = Field(..., max_length=150)
    region: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None


class UniversityResponse(BaseModel):
    university_id: int
    name: str
    region: Optional[str]
    country: Optional[str]
    website: Optional[str]

    class Config:
        orm_mode = True


# Topic Schemas (defined before Course schemas)
class TopicCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class TopicResponse(BaseModel):
    topic_id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


# Course Schemas
class CourseCreate(BaseModel):
    title: str = Field(..., max_length=150)
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    language: Optional[str] = None
    start_date: Optional[date] = None
    duration: Optional[int] = None
    university_id: Optional[int] = None
    quiz_answer_key: Optional[str] = Field(None, max_length=15)


class CourseResponse(BaseModel):
    course_id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    level: Optional[str]
    language: Optional[str]
    duration: Optional[int]
    quiz_answer_key: Optional[str]
    approval_status: Optional[str] = "Approved"

    class Config:
        orm_mode = True


# Instructor Course Creation Schema
class InstructorCourseCreate(BaseModel):
    title: str = Field(..., max_length=150)
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    language: Optional[str] = None
    start_date: Optional[date] = None
    duration: Optional[int] = None
    university_id: Optional[int] = None
    quiz_answer_key: Optional[str] = Field(None, max_length=15)
    topics: List[TopicCreate] = Field(default_factory=list)

    class Config:
        orm_mode = True


class InstructorCourseResponse(BaseModel):
    course_id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    level: Optional[str]
    language: Optional[str]
    duration: Optional[int]
    approval_status: str
    created_by: Optional[int]
    approved_by: Optional[int]
    approved_at: Optional[datetime]

    class Config:
        orm_mode = True