from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import Organization, OrganizationCreate
from app.services import get_organization_service, OrganizationService, get_user_service, UserService
from app.models.schemas import UserCreate, User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    org_service: OrganizationService = Depends(get_organization_service)
):
    """
    Create a new organization (tenant).
    
    This endpoint creates a new organization that will serve as a tenant
    for users and notes. Each organization has its own isolated namespace.
    """
    try:
        # Check if organization with same name already exists
        existing_org = await org_service.get_organization_by_name(org_data.name)
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization with name '{org_data.name}' already exists"
            )
        
        # Create the organization
        organization = await org_service.create_organization(org_data)
        logger.info(f"Created organization: {organization.name} (ID: {organization.id})")
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization"
        )


@router.get("/{org_id}", response_model=Organization)
async def get_organization(
    org_id: str,
    org_service: OrganizationService = Depends(get_organization_service)
):
    """
    Get organization by ID.
    
    Returns the organization details for the given organization ID.
    """
    try:
        organization = await org_service.get_organization_by_id(org_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving organization {org_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organization"
        )


# Bootstrap endpoint removed for security: admin users must be provisioned directly in the database
