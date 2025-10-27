from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.schemas import Note, NoteCreate, NoteUpdate
import logging

logger = logging.getLogger(__name__)


class NoteService:
    """Service for note operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.notes
    
    async def create_note(self, note_data: NoteCreate, organization_id: str, created_by: str) -> Note:
        """Create a new note."""
        if not ObjectId.is_valid(organization_id) or not ObjectId.is_valid(created_by):
            raise ValueError("Invalid organization or user ID")
        
        note_dict = note_data.dict()
        note_dict["organization_id"] = ObjectId(organization_id)
        note_dict["created_by"] = ObjectId(created_by)
        
        result = await self.collection.insert_one(note_dict)
        
        # Fetch the created note
        created_note = await self.collection.find_one({"_id": result.inserted_id})
        return Note(**created_note)
    
    async def get_note_by_id(self, note_id: str) -> Optional[Note]:
        """Get note by ID."""
        if not ObjectId.is_valid(note_id):
            return None
        
        note = await self.collection.find_one({"_id": ObjectId(note_id)})
        return Note(**note) if note else None
    
    async def get_notes_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Note]:
        """Get all notes in an organization."""
        if not ObjectId.is_valid(organization_id):
            return []
        
        cursor = self.collection.find(
            {"organization_id": ObjectId(organization_id)}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        notes = await cursor.to_list(length=None)
        return [Note(**note) for note in notes]
    
    async def update_note(self, note_id: str, note_data: NoteUpdate) -> Optional[Note]:
        """Update note."""
        if not ObjectId.is_valid(note_id):
            return None
        
        update_data = {k: v for k, v in note_data.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.collection.update_one(
                {"_id": ObjectId(note_id)},
                {"$set": update_data}
            )
        
        # Fetch the updated note
        updated_note = await self.collection.find_one({"_id": ObjectId(note_id)})
        return Note(**updated_note) if updated_note else None
    
    async def delete_note(self, note_id: str) -> bool:
        """Delete note."""
        if not ObjectId.is_valid(note_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(note_id)})
        return result.deleted_count > 0
