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
    quiz_answer_key: Optional[str] = Field(None)


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


# Quiz Question Schema for course creation
class QuizQuestionCreate(BaseModel):
    question_text: str
    question_type: str = "multiple_choice"
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None


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
    quiz_answer_key: Optional[str] = Field(None)
    topics: List[TopicCreate] = Field(default_factory=list)
    quiz_questions: List[QuizQuestionCreate] = Field(default_factory=list)

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