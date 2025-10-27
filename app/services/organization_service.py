from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.schemas import Organization, OrganizationCreate
import logging

logger = logging.getLogger(__name__)


class OrganizationService:
    """Service for organization operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.organizations
    
    async def create_organization(self, org_data: OrganizationCreate) -> Organization:
        """Create a new organization."""
        org_dict = org_data.dict()
        result = await self.collection.insert_one(org_dict)
        
        # Fetch the created organization
        created_org = await self.collection.find_one({"_id": result.inserted_id})
        return Organization(**created_org)
    
    async def get_organization_by_id(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID."""
        if not ObjectId.is_valid(org_id):
            return None
        
        org = await self.collection.find_one({"_id": ObjectId(org_id)})
        return Organization(**org) if org else None
    
    async def get_organization_by_name(self, name: str) -> Optional[Organization]:
        """Get organization by name."""
        org = await self.collection.find_one({"name": name})
        return Organization(**org) if org else None
