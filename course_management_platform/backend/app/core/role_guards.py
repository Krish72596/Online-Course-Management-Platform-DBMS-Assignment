# backend/app/core/role_guards.py

from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.core.roles import Role, AdminLevel


# GENERIC ROLE GUARD
def require_role(allowed_roles: list[Role]):

    def role_checker(user=Depends(get_current_user)):

        user_role = user.get("role", "").strip().lower()
        allowed_values = [role.value.lower() for role in allowed_roles]
        
        if user_role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permissions"
            )

        return user

    return role_checker


# ADMIN LEVEL GUARD
def require_admin_level(required_level: AdminLevel):

    def admin_checker(user=Depends(get_current_user)):

        user_role = user.get("role", "").strip().lower()
        
        # Ensure admin role first (case-insensitive)
        if user_role != Role.ADMIN.value.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator access required"
            )

        # Check admin level exists in JWT payload
        user_admin_level = user.get("admin_level", "").strip().lower()
        
        if not user_admin_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin level not found in token. Please log in again. (JWT missing admin_level)"
            )

        # HIERARCHICAL CHECK: Senior >= Junior
        # Senior admins can access both Junior and Senior endpoints
        # Junior admins can only access Junior endpoints
        
        required_level_value = required_level.value.lower()
        
        # Define hierarchy: "senior" > "junior"
        hierarchy = {"junior": 1, "senior": 2}
        
        user_level_rank = hierarchy.get(user_admin_level, 0)
        required_level_rank = hierarchy.get(required_level_value, 0)
        
        # User level must be >= required level
        if user_level_rank < required_level_rank:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient admin level. Required: {required_level.value}, You have: {user_admin_level.capitalize()}"
            )

        return user

    return admin_checker