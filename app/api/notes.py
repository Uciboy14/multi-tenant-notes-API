from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Tuple
from app.models.schemas import Note, NoteCreate, NoteUpdate, User
from app.services import get_note_service, NoteService
from app.core.auth import get_current_user, require_reader, require_writer, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    note_service: NoteService = Depends(get_note_service),
    current_user: Tuple[str, str, User] = Depends(require_writer())
):
    """
    Create a new note.
    
    Only users with writer or admin role can create notes.
    Notes are automatically associated with the user's organization.
    """
    try:
        org_id, user_id, user = current_user
        
        # Create the note
        note = await note_service.create_note(note_data, org_id, user_id)
        logger.info(f"Created note: {note.title} by user {user.email} in organization {org_id}")
        
        return note
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        )


@router.get("/", response_model=List[Note])
async def get_notes(
    skip: int = Query(0, ge=0, description="Number of notes to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of notes to return"),
    note_service: NoteService = Depends(get_note_service),
    current_user: Tuple[str, str, User] = Depends(require_reader())
):
    """
    Get all notes in the user's organization.
    
    All authenticated users can view notes in their organization.
    Notes are returned in descending order by creation date.
    """
    try:
        org_id, user_id, user = current_user
        
        # Get notes for the organization
        notes = await note_service.get_notes_by_organization(org_id, skip, limit)
        
        logger.info(f"Retrieved {len(notes)} notes for user {user.email} in organization {org_id}")
        
        return notes
        
    except Exception as e:
        logger.error(f"Error retrieving notes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notes"
        )


@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: str,
    note_service: NoteService = Depends(get_note_service),
    current_user: Tuple[str, str, User] = Depends(require_reader())
):
    """
    Get a specific note by ID.
    
    All authenticated users can view notes in their organization.
    Users cannot access notes from other organizations.
    """
    try:
        org_id, user_id, user = current_user
        
        # Get the note
        note = await note_service.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        # Verify note belongs to the user's organization
        if str(note.organization_id) != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        logger.info(f"Retrieved note {note_id} for user {user.email}")
        
        return note
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving note {note_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve note"
        )


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    note_service: NoteService = Depends(get_note_service),
    current_user: Tuple[str, str, User] = Depends(require_writer())
):
    """
    Update a note.
    
    Only users with writer or admin role can update notes.
    Users can only update notes in their organization.
    """
    try:
        org_id, user_id, user = current_user
        
        # Get the note
        note = await note_service.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        # Verify note belongs to the user's organization
        if str(note.organization_id) != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        # Update the note
        updated_note = await note_service.update_note(note_id, note_data)
        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        logger.info(f"Updated note {note_id} by user {user.email}")
        
        return updated_note
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating note {note_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update note"
        )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    note_service: NoteService = Depends(get_note_service),
    current_user: Tuple[str, str, User] = Depends(require_admin())
):
    """
    Delete a note.
    
    Only users with admin role can delete notes.
    Users can only delete notes in their organization.
    """
    try:
        org_id, user_id, user = current_user
        
        # Get the note
        note = await note_service.get_note_by_id(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        # Verify note belongs to the user's organization
        if str(note.organization_id) != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        # Delete the note
        deleted = await note_service.delete_note(note_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        logger.info(f"Deleted note {note_id} by admin user {user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting note {note_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note"
        )
