# Quiz System Implementation Guide

## Overview
This document outlines the complete quiz system implementation for the Course Management Platform.

## Architecture

### Data Models
- **Quiz** (`app/models/quiz.py`): Stores quiz metadata for each course
- **QuizQuestion** (`app/models/quiz.py`): Stores individual questions for quizzes
- **Course** (updated): Already has `quiz_answer_key` field for storing answer keys

### Database Tables
```sql
quiz - Stores quiz information per course
  - quiz_id (PK)
  - course_id (FK)
  - title
  - description
  - max_attempts
  - passing_score
  - created_at
  - updated_at

quiz_question - Stores individual questions
  - question_id (PK)
  - quiz_id (FK)
  - question_text
  - question_type (multiple_choice, true_false)
  - option_a, option_b, option_c, option_d
  - correct_answer (A/B/C/D)
  - explanation
  - order
  - created_at
```

## Implementation Components

### Backend

#### 1. Repository Layer (`app/repositories/quiz_repo.py`)
- `create_quiz()`: Create a new quiz for a course
- `get_quiz_by_id()`: Fetch quiz by ID
- `get_quiz_by_course()`: Get quiz for a specific course
- `add_question()`: Add a question to quiz
- `get_questions()`: Get all questions ordered
- `update_question()`: Update question details
- `delete_question()`: Delete a question
- `update_answer_key()`: Update course answer key

#### 2. Service Layer (`app/services/quiz_service.py`)
- `create_or_get_quiz_service()`: Create or retrieve quiz
- `add_question_service()`: Add question with validation
- `get_quiz_questions_service()`: Get quiz with all questions
- `get_quiz_by_course_service()`: Get quiz for display
- `update_answer_key_service()`: Update answer key
- `delete_question_service()`: Delete question

#### 3. Router (`app/routers/quiz.py`)
Available endpoints:

```
POST   /quizzes/course/{course_id}           - Create/get quiz for course
GET    /quizzes/{quiz_id}/questions          - Get all questions
POST   /quizzes/{quiz_id}/questions          - Add question to quiz
GET    /quizzes/course/{course_id}           - Get course quiz
DELETE /quizzes/questions/{question_id}      - Delete question
PUT    /quizzes/courses/{course_id}/answer-key - Update answer key
```

### Frontend

#### 1. Service (`frontend/services/quiz_service.py`)
- `create_quiz_for_course()`: Create/get quiz via API
- `add_question()`: Submit question to backend
- `get_quiz_questions()`: Fetch quiz with questions
- `get_course_quiz()`: Get quiz for displaying to students
- `update_answer_key()`: Update answer key
- `delete_question()`: Delete question

#### 2. UI Components
- **Course Creation** (`frontend/templates/instructor_course_creation.html`):
  - New "Quiz Section" in course creation
  - Add questions one-by-one with validation
  - Input for answer key (string format: "ABCD...")
  - Preview of added questions with delete option

- **Quiz Display** (to be implemented in student dashboard)

## Usage Flow

### Instructor: Creating a Course with Quiz

1. Navigate to course creation page
2. Fill course details (title, description, etc.)
3. Add course topics
4. **NEW**: Scroll to "Final Test / Quiz" section
5. Add questions:
   - Enter question text
   - Select question type (Multiple Choice/True-False)
   - Add options A, B, C, D
   - Select correct answer
   - (Optional) Add explanation
   - Click "+ Add Question"
6. Enter answer key (matching number of questions)
   - Example: "CBACAAABACBACAC" for 15 questions
7. Submit course

### System: Automatic Quiz Creation

When course is created:
1. Quiz table entry is created with generic title "Final Test"
2. Answer key is stored in `course.quiz_answer_key`
3. Questions are stored in `quiz_question` table in order

### Student: Taking Quiz (Future Implementation)

1. Navigate to course detail page
2. See "Take Quiz" button
3. Quiz loads dynamically from database (not hardcoded)
4. Student answers questions
5. Submit answers
6. System evaluates against stored answer key
7. Display results

## Database Setup

### Create Tables
Run the migration SQL:
```bash
psql -U user -d course_management_db < backend/database/migrations/add_quiz_tables.sql
```

### Dummy Data
The migration script automatically:
1. Creates a quiz for the first course (if it exists)
2. Adds 15 sample questions
3. Sets answer key: "CBACAAABACBACAC"
4. Clones same quiz for all other existing courses
5. Updates answer key for all courses

### Constraints
The SQL migration includes:
- Foreign key constraints (CASCADE delete)
- Indexes for performance
- NOT NULL constraints on required fields
- Default values for settings

## File Structure

```
backend/
  ├── app/
  │   ├── models/
  │   │   └── quiz.py              # Data models
  │   ├── repositories/
  │   │   └── quiz_repo.py         # Database operations
  │   ├── services/
  │   │   └── quiz_service.py      # Business logic
  │   └── routers/
  │       └── quiz.py              # API endpoints
  └── database/
      └── migrations/
          └── add_quiz_tables.sql  # Schema + dummy data

frontend/
  ├── services/
  │   └── quiz_service.py          # API client
  └── templates/
      ├── instructor_course_creation.html    # Updated with quiz
      ├── quiz_section.html        # Quiz component
      └── (future) student_quiz.html # Quiz display
```

## Integration Checklist

- [x] Create data models (Quiz, QuizQuestion)
- [x] Create repository layer
- [x] Create service layer
- [x] Create API routes
- [x] Register routes in main.py
- [x] Create frontend service
- [x] Add quiz section to course creation form
- [x] Add JavaScript for question management
- [x] Create database migration with dummy data
- [ ] Create student quiz taker interface
- [ ] Add quiz grading logic
- [ ] Add quiz history/results tracking

## Future Enhancements

1. **Quiz Attempts**: Track student attempts and scores
2. **Randomize Questions**: Shuffle questions for fairness
3. **Partial Credit**: Weighted scoring for questions
4. **Timed Quizzes**: Add time limits
5. **Question Banks**: Reuse questions across courses
6. **Analytics**: Track student performance
7. **Review Mode**: Let students review after submission

## API Examples

### Create Quiz for Course
```bash
POST /quizzes/course/1
Authorization: Bearer {token}
```

### Add Question
```bash
POST /quizzes/1/questions
Authorization: Bearer {token}
{
    "question_text": "What is 2+2?",
    "question_type": "multiple_choice",
    "option_a": "3",
    "option_b": "4",
    "option_c": "5",
    "option_d": "6",
    "correct_answer": "B",
    "explanation": "The sum of 2 and 2 is 4"
}
```

### Get Quiz Questions
```bash
GET /quizzes/1/questions
Authorization: Bearer {token}
```

### Get Course Quiz (for students)
```bash
GET /quizzes/course/1
Authorization: Bearer {token}  # Optional for public view
```

### Update Answer Key
```bash
PUT /quizzes/courses/1/answer-key
Authorization: Bearer {token}
{
    "quiz_answer_key": "ABCDACBDABCDABC"
}
```
