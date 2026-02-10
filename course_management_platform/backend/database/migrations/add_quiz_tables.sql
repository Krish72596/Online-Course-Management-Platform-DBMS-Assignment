-- ============================================================
-- QUIZ AND QUIZ_QUESTION TABLES
-- ============================================================

-- Create quiz table
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

-- Create quiz_question table
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

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_quiz_course_id ON quiz(course_id);
CREATE INDEX IF NOT EXISTS idx_quiz_question_quiz_id ON quiz_question(quiz_id);

-- ============================================================
-- DUMMY DATA
-- ============================================================

-- Get the first course_id (assuming courses already exist)
-- Insert quiz for course 1 (if it exists)
DO $$ 
DECLARE
    first_course_id INT;
    new_quiz_id INT;
    course_count INT;
BEGIN
    -- Check if courses exist
    SELECT COUNT(*) INTO course_count FROM course;
    
    IF course_count > 0 THEN
        -- Get the first course
        SELECT course_id INTO first_course_id FROM course LIMIT 1;
        
        -- Insert quiz for this course if it doesn't already have one
        INSERT INTO quiz (course_id, title, description, max_attempts, passing_score)
        SELECT first_course_id, 'Final Test', 'Final assessment quiz for this course', 1, 70
        WHERE NOT EXISTS (
            SELECT 1 FROM quiz WHERE course_id = first_course_id
        )
        RETURNING quiz_id INTO new_quiz_id;
        
        -- If the insert succeeded, new_quiz_id will have a value
        IF new_quiz_id IS NOT NULL THEN
            -- Insert 15 sample questions for this quiz
            INSERT INTO quiz_question (quiz_id, question_text, question_type, option_a, option_b, option_c, option_d, correct_answer, explanation, "order")
            VALUES
                (new_quiz_id, 'What is the capital of France?', 'multiple_choice', 'London', 'Berlin', 'Paris', 'Madrid', 'C', 'Paris is the capital of France.', 1),
                (new_quiz_id, 'What is 2 + 2?', 'multiple_choice', '3', '4', '5', '6', 'B', 'The sum of 2 and 2 is 4.', 2),
                (new_quiz_id, 'Who wrote Romeo and Juliet?', 'multiple_choice', 'Jane Austen', 'William Shakespeare', 'Charles Dickens', 'Mark Twain', 'B', 'William Shakespeare wrote Romeo and Juliet.', 3),
                (new_quiz_id, 'What is the largest planet in our solar system?', 'multiple_choice', 'Saturn', 'Jupiter', 'Neptune', 'Earth', 'B', 'Jupiter is the largest planet in our solar system.', 4),
                (new_quiz_id, 'In what year did the Titanic sink?', 'multiple_choice', '1912', '1915', '1920', '1925', 'A', 'The Titanic sank in 1912.', 5),
                (new_quiz_id, 'What is the chemical symbol for gold?', 'multiple_choice', 'Go', 'Gd', 'Au', 'Ag', 'C', 'The chemical symbol for gold is Au.', 6),
                (new_quiz_id, 'Who is the author of the Harry Potter series?', 'multiple_choice', 'George R.R. Martin', 'J.K. Rowling', 'Stephenie Meyer', 'Veronica Roth', 'B', 'J.K. Rowling wrote the Harry Potter series.', 7),
                (new_quiz_id, 'What is the smallest country in the world?', 'multiple_choice', 'Monaco', 'Liechtenstein', 'Vatican City', 'San Marino', 'C', 'Vatican City is the smallest country in the world.', 8),
                (new_quiz_id, 'What does DNA stand for?', 'multiple_choice', 'Deoxyribonucleic Acid', 'Diribonucleic Acid', 'Deoxyribose Nucleic', 'Dynamic Nucleic Acid', 'A', 'DNA stands for Deoxyribonucleic Acid.', 9),
                (new_quiz_id, 'In what country is the Great Wall located?', 'multiple_choice', 'Japan', 'South Korea', 'China', 'Vietnam', 'C', 'The Great Wall is located in China.', 10),
                (new_quiz_id, 'What is the hardest natural substance on Earth?', 'multiple_choice', 'Gold', 'Diamond', 'Platinum', 'Graphite', 'B', 'Diamond is the hardest natural substance on Earth.', 11),
                (new_quiz_id, 'Who was the first President of the United States?', 'multiple_choice', 'Thomas Jefferson', 'Benjamin Franklin', 'George Washington', 'John Adams', 'C', 'George Washington was the first President of the United States.', 12),
                (new_quiz_id, 'What is the speed of light?', 'multiple_choice', '300,000 km/s', '150,000 km/s', '600,000 km/s', '1,000,000 km/s', 'A', 'The speed of light is approximately 300,000 kilometers per second.', 13),
                (new_quiz_id, 'How many continents are there?', 'multiple_choice', '5', '6', '7', '8', 'C', 'There are 7 continents on Earth.', 14),
                (new_quiz_id, 'What is the most spoken language in the world?', 'multiple_choice', 'Spanish', 'English', 'Mandarin Chinese', 'Hindi', 'C', 'Mandarin Chinese is the most spoken language in the world by native speakers.', 15);
        ELSE
            -- Get the existing quiz ID instead
            SELECT quiz_id INTO new_quiz_id FROM quiz WHERE course_id = first_course_id LIMIT 1;
        END IF;
        
        -- Update answer key for the course
        UPDATE course SET quiz_answer_key = 'CBACAAABACBACAC' WHERE course_id = first_course_id;
    END IF;
END $$;

-- For all other courses, insert the same quiz and questions
DO $$
DECLARE
    course_rec RECORD;
    v_new_quiz_id INT;
    v_first_quiz_id INT;
BEGIN
    -- Get the first quiz as template
    SELECT quiz_id INTO v_first_quiz_id FROM quiz LIMIT 1;
    
    IF v_first_quiz_id IS NOT NULL THEN
        -- For each course that doesn't have a quiz
        FOR course_rec IN
            SELECT c.course_id FROM course c
            WHERE NOT EXISTS (
                SELECT 1 FROM quiz q WHERE q.course_id = c.course_id
            )
        LOOP
            -- Create a new quiz with same settings
            INSERT INTO quiz (course_id, title, description, max_attempts, passing_score)
            VALUES (course_rec.course_id, 'Final Test', 'Final assessment quiz for this course', 1, 70)
            RETURNING quiz_id INTO v_new_quiz_id;
            
            -- Insert the same 15 questions for this quiz
            INSERT INTO quiz_question (quiz_id, question_text, question_type, option_a, option_b, option_c, option_d, correct_answer, explanation, "order")
            SELECT
                v_new_quiz_id,
                question_text,
                question_type,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                explanation,
                "order"
            FROM quiz_question
            WHERE quiz_id = v_first_quiz_id;
            
            -- Update answer key for this course
            UPDATE course SET quiz_answer_key = 'CBACAAABACBACAC' WHERE course_id = course_rec.course_id;
        END LOOP;
    END IF;
END $$;
