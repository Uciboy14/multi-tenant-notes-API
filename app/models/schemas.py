from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler
from pydantic_core import core_schema
from datetime import datetime
from bson import ObjectId


class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2 models."""
    
    @classmethod
    def __get_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if ObjectId.is_valid(value):
                return str(value)
            raise ValueError("Invalid ObjectId")
        
        return core_schema.no_info_plain_validator_function(validate)


class UserRole(str, Enum):
    """User roles with their permissions."""
    READER = "reader"
    WRITER = "writer"
    ADMIN = "admin"


class OrganizationBase(BaseModel):
    """Base organization model."""
    name: str = Field(..., min_length=1, max_length=100)


class OrganizationCreate(OrganizationBase):
    """Organization creation model."""
    pass


class Organization(OrganizationBase):
    """Organization model with ID and timestamps."""
    id: str = Field(default="", alias="_id")
    created_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "by_alias": True,
        "arbitrary_types_allowed": True,
    }


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation model."""
    role: UserRole = UserRole.READER


class UserUpdate(BaseModel):
    """User update model."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None


class User(UserBase):
    """User model with ID, role, and timestamps."""
    id: str = Field(default="", alias="_id")
    organization_id: str
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "populate_by_name": True,
        "by_alias": True,
        "arbitrary_types_allowed": True,
    }


class NoteBase(BaseModel):
    """Base note model."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NoteCreate(NoteBase):
    """Note creation model."""
    pass


class NoteUpdate(BaseModel):
    """Note update model."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class Note(NoteBase):
    """Note model with ID, organization, and timestamps."""
    id: str = Field(default="", alias="_id")
    organization_id: str
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "populate_by_name": True,
        "by_alias": True,
        "arbitrary_types_allowed": True,
    }


class AuthHeaders(BaseModel):
    """Authentication headers model."""
    org_id: str = Field(..., alias="X-Org-ID")
    user_id: str = Field(..., alias="X-User-ID")
    
    model_config = {
        "populate_by_name": True,
    }


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    error_code: Optional[str] = None
