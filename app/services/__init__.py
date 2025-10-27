"""Service factory functions for dependency injection."""
from app.services.organization_service import OrganizationService
from app.services.user_service import UserService
from app.services.note_service import NoteService
from app.core.database import get_database


async def get_organization_service() -> OrganizationService:
    """Get organization service instance."""
    db = await get_database()
    return OrganizationService(db)


async def get_user_service() -> UserService:
    """Get user service instance."""
    db = await get_database()
    return UserService(db)


async def get_note_service() -> NoteService:
    """Get note service instance."""
    db = await get_database()
    return NoteService(db)