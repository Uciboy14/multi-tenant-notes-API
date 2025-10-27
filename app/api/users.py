from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Tuple
from app.models.schemas import User, UserCreate, UserUpdate, UserRole
from app.services import get_user_service, UserService, get_organization_service, OrganizationService
from app.core.auth import get_current_user, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    org_id: str,
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    org_service: OrganizationService = Depends(get_organization_service),
    current_user: Tuple[str, str, User] = Depends(require_admin())
):
    """
    Create a new user under a specific organization.
    
    Only admin users can create new users. The user will be assigned
    to the specified organization with the given role.
    """
    try:
        # Verify organization exists
        organization = await org_service.get_organization_by_id(org_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Check if user with same email already exists in this organization
        existing_user = await user_service.get_user_by_email_and_org(user_data.email, org_id)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{user_data.email}' already exists in this organization"
            )
        
        # Create the user
        user = await user_service.create_user(user_data, org_id)
        logger.info(f"Created user: {user.email} in organization {org_id} with role {user.role}")
        
        return user
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/", response_model=List[User])
async def get_users(
    org_id: str,
    user_service: UserService = Depends(get_user_service),
    org_service: OrganizationService = Depends(get_organization_service),
    current_user: Tuple[str, str, User] = Depends(require_admin())
):
    """
    Get all users in an organization.
    
    Only admin users can view all users in an organization.
    """
    try:
        # Verify organization exists
        organization = await org_service.get_organization_by_id(org_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Get all users in the organization
        users = await user_service.get_users_by_organization(org_id)
        
        return users
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving users for organization {org_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/{user_id}", response_model=User)
async def get_user(
    org_id: str,
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    current_user: Tuple[str, str, User] = Depends(require_admin())
):
    """
    Get a specific user by ID.
    
    Only admin users can view user details.
    """
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify user belongs to the organization
        if str(user.organization_id) != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in this organization"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.put("/{user_id}", response_model=User)
async def update_user(
    org_id: str,
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: Tuple[str, str, User] = Depends(require_admin())
):
    """
    Update user information.
    
    Only admin users can update user information.
    """
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify user belongs to the organization
        if str(user.organization_id) != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in this organization"
            )
        
        # Update the user
        updated_user = await user_service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Updated user: {updated_user.email} in organization {org_id}")
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
