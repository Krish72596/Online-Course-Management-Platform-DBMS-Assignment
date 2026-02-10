import requests
import os
from typing import Dict, Any, Tuple

BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')


class AnalystService:
    """Service for handling data analyst dashboard API calls"""
    
    @staticmethod
    def get_platform_overview(token: str) -> Tuple[bool, Dict[str, Any]]:
        """Get platform-wide overview statistics"""
        try:
            response = requests.get(
                f'{BACKEND_URL}/analyst/overview',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}
        except requests.exceptions.RequestException as e:
            return False, {}
    
    @staticmethod
    def get_all_courses_analytics(token: str) -> Tuple[bool, Dict[str, Any]]:
        """Get analytics for all courses"""
        try:
            response = requests.get(
                f'{BACKEND_URL}/analyst/courses/analytics',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}
        except requests.exceptions.RequestException as e:
            return False, {}
    
    @staticmethod
    def get_course_detailed_analytics(course_id: int, token: str) -> Tuple[bool, Dict[str, Any]]:
        """Get detailed analytics for a specific course"""
        try:
            response = requests.get(
                f'{BACKEND_URL}/analyst/courses/{course_id}/detailed',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}
        except requests.exceptions.RequestException as e:
            return False, {}
    
    @staticmethod
    def get_all_students_analytics(token: str) -> Tuple[bool, Dict[str, Any]]:
        """Get analytics for all students"""
        try:
            response = requests.get(
                f'{BACKEND_URL}/analyst/students/analytics',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}
        except requests.exceptions.RequestException as e:
            return False, {}
    
    @staticmethod
    def get_all_instructors_analytics(token: str) -> Tuple[bool, Dict[str, Any]]:
        """Get analytics for all instructors"""
        try:
            response = requests.get(
                f'{BACKEND_URL}/analyst/instructors/analytics',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {}
        except requests.exceptions.RequestException as e:
            return False, {}
