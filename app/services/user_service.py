from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.schemas import User, UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users
    
    async def create_user(self, user_data: UserCreate, organization_id: str) -> User:
        """Create a new user under an organization."""
        if not ObjectId.is_valid(organization_id):
            raise ValueError("Invalid organization ID")
        
        user_dict = user_data.dict()
        user_dict["organization_id"] = ObjectId(organization_id)
        
        result = await self.collection.insert_one(user_dict)
        
        # Fetch the created user
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return User(**created_user)
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        if not ObjectId.is_valid(user_id):
            return None
        
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return User(**user) if user else None
    
    async def get_user_by_email_and_org(self, email: str, organization_id: str) -> Optional[User]:
        """Get user by email and organization."""
        if not ObjectId.is_valid(organization_id):
            return None
        
        user = await self.collection.find_one({
            "email": email,
            "organization_id": ObjectId(organization_id)
        })
        return User(**user) if user else None
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user information."""
        if not ObjectId.is_valid(user_id):
            return None
        
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
        
        # Fetch the updated user
        updated_user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return User(**updated_user) if updated_user else None
    
    async def get_users_by_organization(self, organization_id: str) -> List[User]:
        """Get all users in an organization."""
        if not ObjectId.is_valid(organization_id):
            return []
        
        cursor = self.collection.find({"organization_id": ObjectId(organization_id)})
        users = await cursor.to_list(length=None)
        return [User(**user) for user in users]
