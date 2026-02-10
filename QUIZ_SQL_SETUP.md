# Quick SQL Setup Guide for Quiz System

## One-Command Setup

Run this to set up everything:

```bash
psql -U your_username -d course_management_db < backend/database/migrations/add_quiz_tables.sql
```

---

## Manual Setup (If needed)

### Step 1: Create Quiz Table

```sql
CREATE TABLE IF NOT EXISTS quiz (
    quiz_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES course(course_id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    max_attempts INTEGER DEFAULT 1,
    passing_score INTEGER DEFAULT 70,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quiz_course_id ON quiz(course_id);
```

### Step 2: Create Quiz Question Table

```sql
CREATE TABLE IF NOT EXISTS quiz_question (
    question_id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quiz(quiz_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(20) DEFAULT 'multiple_choice',
    option_a VARCHAR(255),
    option_b VARCHAR(255),
    option_c VARCHAR(255),
    option_d VARCHAR(255),
    correct_answer VARCHAR(1) NOT NULL,
    explanation TEXT,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quiz_question_quiz_id ON quiz_question(quiz_id);
```

### Step 3: Insert Sample Quiz and Questions

```sql
-- Get first course ID
SELECT course_id FROM course LIMIT 1;

-- Insert quiz (replace 1 with actual course_id)
INSERT INTO quiz (course_id, title, description, max_attempts, passing_score)
VALUES (1, 'Final Test', 'Final assessment quiz for this course', 1, 70)
RETURNING quiz_id;

-- Get the quiz_id from above and use it below (replace 1)
-- Insert 15 sample questions
INSERT INTO quiz_question (quiz_id, question_text, question_type, option_a, option_b, option_c, option_d, correct_answer, explanation, "order")
VALUES
(1, 'What is the capital of France?', 'multiple_choice', 'London', 'Berlin', 'Paris', 'Madrid', 'C', 'Paris is the capital of France.', 1),
(1, 'What is 2 + 2?', 'multiple_choice', '3', '4', '5', '6', 'B', 'The sum of 2 and 2 is 4.', 2),
(1, 'Who wrote Romeo and Juliet?', 'multiple_choice', 'Jane Austen', 'William Shakespeare', 'Charles Dickens', 'Mark Twain', 'B', 'William Shakespeare wrote Romeo and Juliet.', 3),
(1, 'What is the largest planet in our solar system?', 'multiple_choice', 'Saturn', 'Jupiter', 'Neptune', 'Earth', 'B', 'Jupiter is the largest planet in our solar system.', 4),
(1, 'In what year did the Titanic sink?', 'multiple_choice', '1912', '1915', '1920', '1925', 'A', 'The Titanic sank in 1912.', 5),
(1, 'What is the chemical symbol for gold?', 'multiple_choice', 'Go', 'Gd', 'Au', 'Ag', 'C', 'The chemical symbol for gold is Au.', 6),
(1, 'Who is the author of the Harry Potter series?', 'multiple_choice', 'George R.R. Martin', 'J.K. Rowling', 'Stephenie Meyer', 'Veronica Roth', 'B', 'J.K. Rowling wrote the Harry Potter series.', 7),
(1, 'What is the smallest country in the world?', 'multiple_choice', 'Monaco', 'Liechtenstein', 'Vatican City', 'San Marino', 'C', 'Vatican City is the smallest country in the world.', 8),
(1, 'What does DNA stand for?', 'multiple_choice', 'Deoxyribonucleic Acid', 'Diribonucleic Acid', 'Deoxyribose Nucleic', 'Dynamic Nucleic Acid', 'A', 'DNA stands for Deoxyribonucleic Acid.', 9),
(1, 'In what country is the Great Wall located?', 'multiple_choice', 'Japan', 'South Korea', 'China', 'Vietnam', 'C', 'The Great Wall is located in China.', 10),
(1, 'What is the hardest natural substance on Earth?', 'multiple_choice', 'Gold', 'Diamond', 'Platinum', 'Graphite', 'B', 'Diamond is the hardest natural substance on Earth.', 11),
(1, 'Who was the first President of the United States?', 'multiple_choice', 'Thomas Jefferson', 'Benjamin Franklin', 'George Washington', 'John Adams', 'C', 'George Washington was the first President of the United States.', 12),
(1, 'What is the speed of light?', 'multiple_choice', '300,000 km/s', '150,000 km/s', '600,000 km/s', '1,000,000 km/s', 'A', 'The speed of light is approximately 300,000 kilometers per second.', 13),
(1, 'How many continents are there?', 'multiple_choice', '5', '6', '7', '8', 'C', 'There are 7 continents on Earth.', 14),
(1, 'What is the most spoken language in the world?', 'multiple_choice', 'Spanish', 'English', 'Mandarin Chinese', 'Hindi', 'C', 'Mandarin Chinese is the most spoken language in the world by native speakers.', 15);
```

### Step 4: Update Courses with Answer Key

```sql
-- Update answer key for the course (replace 1 with course_id)
UPDATE course SET quiz_answer_key = 'CBACAAABACBACAC' WHERE course_id = 1;

-- Or update all courses
UPDATE course SET quiz_answer_key = 'CBACAAABACBACAC';
```

---

## Verify Setup

```sql
-- Check if quiz table created
SELECT COUNT(*) FROM quiz;

-- Check if questions inserted
SELECT COUNT(*) FROM quiz_question;

-- View quiz info
SELECT * FROM quiz WHERE course_id = 1;

-- View questions for quiz
SELECT * FROM quiz_question WHERE quiz_id = 1 ORDER BY "order";

-- Check course answer key
SELECT course_id, quiz_answer_key FROM course LIMIT 5;
```

---

## Expected Output

### After Creating Quiz Table
```
CREATE TABLE
CREATE INDEX
```

### After Creating Questions Table
```
CREATE TABLE
CREATE INDEX
```

### After Inserting 15 Questions
```
INSERT 0 1    (for quiz insert)
INSERT 0 15   (for questions insert)
```

### Verification Queries
```
 count
-------
     1        (1 quiz created)

 count
-------
    15        (15 questions created)

 quiz_id | course_id | title       | description                          | max_attempts | passing_score
---------+-----------+-------------|--------------------------------------+--------------+----------------
       1 |         1 | Final Test  | Final assessment quiz for this course|            1 |             70
```

---

## Troubleshooting

### Table Already Exists
If you get "table already exists" error:
```sql
-- Drop and recreate (WARNING: loses all data)
DROP TABLE IF EXISTS quiz_question CASCADE;
DROP TABLE IF EXISTS quiz CASCADE;

-- Then run the CREATE statements above
```

### Foreign Key Constraint Error
This means the course_id doesn't exist:
```sql
-- Check available course IDs
SELECT course_id, title FROM course LIMIT 10;

-- Use an existing course_id in the INSERT statement
```

### Answer Key Format Error
Answer key must be:
- Only uppercase letters (A, B, C, D)
- Matching number of questions
- Example for 15 questions: `CBACAAABACBACAC`

```sql
-- Validate answer key length
SELECT course_id, quiz_answer_key, 
       length(quiz_answer_key) as "key_length",
       (SELECT COUNT(*) FROM quiz_question WHERE quiz_id = q.quiz_id) as "question_count"
FROM course c
JOIN quiz q ON c.course_id = q.course_id
LIMIT 5;
```

---

## Backup Before Testing

```bash
# Create backup
pg_dump course_management_db > backup_before_quiz.sql

# Run migration
psql -U username -d course_management_db < backend/database/migrations/add_quiz_tables.sql

# If needed, restore backup
psql -U username -d course_management_db < backup_before_quiz.sql
```

---

## Next Steps After SQL Setup

1. **Verify Tables**: Run verification queries above
2. **Restart Backend**: Kill and restart uvicorn server
3. **Test API**: Open http://127.0.0.1:8000/docs and test `/quizzes/course/1` endpoint
4. **Test UI**: Go to course detail page and try "Take Quiz"
5. **Create New Course**: Test course creation with quiz section

---

## Full Setup in One Go

```bash
#!/bin/bash

echo "Creating backup..."
pg_dump course_management_db > backup_$(date +%Y%m%d_%H%M%S).sql

echo "Running migration..."
psql -U your_username -d course_management_db < backend/database/migrations/add_quiz_tables.sql

echo "Verifying setup..."
psql -U your_username -d course_management_db -c "SELECT COUNT(*) AS quiz_count FROM quiz; SELECT COUNT(*) AS question_count FROM quiz_question;"

echo "Setup complete!"
```

Makeexecutable:
```bash
chmod +x setup_quiz.sh
./setup_quiz.sh
```
