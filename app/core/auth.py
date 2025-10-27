from fastapi import HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Tuple, Callable
from bson import ObjectId
from app.models.schemas import UserRole, User
from app.services import get_user_service, UserService
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


class TenantAuthMiddleware(BaseHTTPMiddleware):
    """Middleware that automatically extracts tenant/user from headers for every request."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Extract and validate tenant/user information from headers on every request."""
        
        # Skip auth middleware for public endpoints
        public_endpoints = ["/health", "/", "/docs", "/openapi.json", "/redoc"]
        
        # Allow ALL organization endpoints without auth (public API)
        if request.url.path.startswith("/organizations/"):
            return await call_next(request)
        
        # Allow other public endpoints
        elif any(request.url.path.startswith(endpoint) for endpoint in public_endpoints):
            return await call_next(request)
        
        # Extract headers
        org_id = request.headers.get("X-Org-ID")
        user_id = request.headers.get("X-User-ID")
        
        if not org_id or not user_id:
            return Response(
                status_code=401,
                content='{"detail": "Missing required headers: X-Org-ID and X-User-ID"}',
                media_type="application/json"
            )
        
        # Validate ObjectId format
        if not ObjectId.is_valid(org_id) or not ObjectId.is_valid(user_id):
            return Response(
                status_code=400,
                content='{"detail": "Invalid organization or user ID format"}',
                media_type="application/json"
            )
        
        # Store validated IDs in request state for use in endpoints
        request.state.org_id = org_id
        request.state.user_id = user_id
        
        # Continue to the next middleware/endpoint
        response = await call_next(request)
        return response


class AuthMiddleware:
    """Authentication middleware for extracting tenant and user information."""
    
    @staticmethod
    async def get_current_user(
        request: Request,
        x_org_id: str = Header(..., alias="X-Org-ID", description="Organization ID (MongoDB ObjectId)"),
        x_user_id: str = Header(..., alias="X-User-ID", description="User ID (MongoDB ObjectId)"),
        user_service: UserService = Depends(get_user_service)
    ) -> Tuple[str, str, User]:
        """
        Extract and validate user information from headers.
        
        **Required Headers:**
        - X-Org-ID: Your organization ID
        - X-User-ID: Your user ID
        
        Returns tuple of (org_id, user_id, user_object).
        """
        # Extract headers (already validated by FastAPI Header)
        org_id = x_org_id
        user_id = x_user_id
        
        # Validate ObjectId format
        if not ObjectId.is_valid(org_id) or not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid organization or user ID format"
            )
        
        # Get user from database
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Verify user belongs to the organization
        if str(user.organization_id) != org_id:
            raise HTTPException(
                status_code=403,
                detail="User does not belong to the specified organization"
            )
        
        return org_id, user_id, user


class RoleBasedAccessControl:
    """Role-based access control for API endpoints."""
    
    @staticmethod
    def require_role(allowed_roles: list[UserRole]):
        """Decorator to require specific roles for access."""
        def role_checker(current_user: Tuple[str, str, User] = Depends(AuthMiddleware.get_current_user)):
            org_id, user_id, user = current_user
            
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}, "
                           f"user role: {user.role.value}"
                )
            
            return current_user
        
        return role_checker
    
    @staticmethod
    def require_reader_access():
        """Require reader role or higher."""
        return RoleBasedAccessControl.require_role([UserRole.READER, UserRole.WRITER, UserRole.ADMIN])
    
    @staticmethod
    def require_writer_access():
        """Require writer role or higher."""
        return RoleBasedAccessControl.require_role([UserRole.WRITER, UserRole.ADMIN])
    
    @staticmethod
    def require_admin_access():
        """Require admin role."""
        return RoleBasedAccessControl.require_role([UserRole.ADMIN])


# Convenience functions for dependency injection
async def get_current_user(
    request: Request,
    user_service: UserService = Depends(get_user_service)
) -> Tuple[str, str, User]:
    """Get current authenticated user."""
    return await AuthMiddleware.get_current_user(request, user_service)


def require_reader():
    """Dependency for reader access."""
    return RoleBasedAccessControl.require_reader_access()


def require_writer():
    """Dependency for writer access."""
    return RoleBasedAccessControl.require_writer_access()


def require_admin():
    """Dependency for admin access."""
    return RoleBasedAccessControl.require_admin_access()
