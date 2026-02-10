import requests
import os
from typing import Dict, Any, Tuple

BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')


class QuizService:
    """Service for handling quiz-related API calls"""
    
    @staticmethod
    def create_quiz_for_course(course_id: int, token: str) -> Tuple[bool, Any]:
        """Create or get a quiz for a course"""
        try:
            resp = requests.post(
                f"{BACKEND_URL}/quizzes/course/{course_id}",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def add_question(quiz_id: int, question_data: Dict, token: str) -> Tuple[bool, Any]:
        """Add a question to a quiz"""
        try:
            resp = requests.post(
                f"{BACKEND_URL}/quizzes/{quiz_id}/questions",
                json=question_data,
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.json() if resp.text else None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def get_quiz_questions(quiz_id: int, token: str = None) -> Tuple[bool, Any]:
        """Get all questions for a quiz"""
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            resp = requests.get(
                f"{BACKEND_URL}/quizzes/{quiz_id}/questions",
                headers=headers,
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def get_course_quiz(course_id: int, token: str = None) -> Tuple[bool, Any]:
        """Get quiz for a specific course"""
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            resp = requests.get(
                f"{BACKEND_URL}/quizzes/course/{course_id}",
                headers=headers,
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def update_answer_key(course_id: int, answer_key: str, token: str) -> Tuple[bool, Any]:
        """Update answer key for a course"""
        try:
            resp = requests.put(
                f"{BACKEND_URL}/quizzes/courses/{course_id}/answer-key",
                json={'quiz_answer_key': answer_key},
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.json() if resp.text else None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
    
    @staticmethod
    def delete_question(question_id: int, token: str) -> Tuple[bool, Any]:
        """Delete a question from a quiz"""
        try:
            resp = requests.delete(
                f"{BACKEND_URL}/quizzes/questions/{question_id}",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, None
        except requests.exceptions.RequestException as e:
            return False, {'error': str(e)}
