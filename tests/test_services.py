import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.services import OrganizationService, UserService, NoteService
from app.models.schemas import OrganizationCreate, UserCreate, NoteCreate, UserRole
from app.core.database import connect_to_mongo, close_mongo_connection, get_database
from app.core.config import settings
from bson import ObjectId


@pytest.fixture(scope="function")
async def test_db():
    """Create a test database connection."""
    test_url = "mongodb://localhost:27017/notes_api_test"
    settings.mongodb_url = test_url
    settings.database_name = "notes_api_test"
    
    await connect_to_mongo()
    yield
    await close_mongo_connection()


@pytest.fixture
async def clean_db(test_db):
    """Clean the test database before each test."""
    db = await get_database()
    await db.organizations.delete_many({})
    await db.users.delete_many({})
    await db.notes.delete_many({})
    yield
    # Clean up after test
    await db.organizations.delete_many({})
    await db.users.delete_many({})
    await db.notes.delete_many({})


@pytest.fixture
async def organization_service(clean_db):
    """Create organization service instance."""
    db = await get_database()
    return OrganizationService(db)


@pytest.fixture
async def user_service(clean_db):
    """Create user service instance."""
    db = await get_database()
    return UserService(db)


@pytest.fixture
async def note_service(clean_db):
    """Create note service instance."""
    db = await get_database()
    return NoteService(db)


class TestOrganizationService:
    """Test cases for OrganizationService."""
    
    async def test_create_organization(self, organization_service):
        """Test creating a new organization."""
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        assert organization.name == "Test Organization"
        assert organization.id is not None
        assert organization.created_at is not None
    
    async def test_get_organization_by_id(self, organization_service):
        """Test retrieving organization by ID."""
        org_data = OrganizationCreate(name="Test Organization")
        created_org = await organization_service.create_organization(org_data)
        
        retrieved_org = await organization_service.get_organization_by_id(str(created_org.id))
        
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == created_org.name
    
    async def test_get_organization_by_name(self, organization_service):
        """Test retrieving organization by name."""
        org_data = OrganizationCreate(name="Test Organization")
        created_org = await organization_service.create_organization(org_data)
        
        retrieved_org = await organization_service.get_organization_by_name("Test Organization")
        
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == created_org.name
    
    async def test_get_nonexistent_organization(self, organization_service):
        """Test retrieving non-existent organization."""
        fake_id = str(ObjectId())
        retrieved_org = await organization_service.get_organization_by_id(fake_id)
        
        assert retrieved_org is None


class TestUserService:
    """Test cases for UserService."""
    
    async def test_create_user(self, user_service, organization_service):
        """Test creating a new user."""
        # First create an organization
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        # Create a user
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            role=UserRole.READER
        )
        user = await user_service.create_user(user_data, str(organization.id))
        
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.READER
        assert user.organization_id == organization.id
        assert user.id is not None
    
    async def test_get_user_by_id(self, user_service, organization_service):
        """Test retrieving user by ID."""
        # Create organization and user
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            role=UserRole.READER
        )
        created_user = await user_service.create_user(user_data, str(organization.id))
        
        # Retrieve user
        retrieved_user = await user_service.get_user_by_id(str(created_user.id))
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
    
    async def test_get_user_by_email_and_org(self, user_service, organization_service):
        """Test retrieving user by email and organization."""
        # Create organization and user
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            role=UserRole.READER
        )
        created_user = await user_service.create_user(user_data, str(organization.id))
        
        # Retrieve user by email and org
        retrieved_user = await user_service.get_user_by_email_and_org(
            "test@example.com", str(organization.id)
        )
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
    
    async def test_get_users_by_organization(self, user_service, organization_service):
        """Test retrieving all users in an organization."""
        # Create organization
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        # Create multiple users
        users_data = [
            UserCreate(email="user1@example.com", name="User 1", role=UserRole.READER),
            UserCreate(email="user2@example.com", name="User 2", role=UserRole.WRITER),
            UserCreate(email="user3@example.com", name="User 3", role=UserRole.ADMIN),
        ]
        
        for user_data in users_data:
            await user_service.create_user(user_data, str(organization.id))
        
        # Retrieve all users
        users = await user_service.get_users_by_organization(str(organization.id))
        
        assert len(users) == 3
        emails = [user.email for user in users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@example.com" in emails


class TestNoteService:
    """Test cases for NoteService."""
    
    async def test_create_note(self, note_service, user_service, organization_service):
        """Test creating a new note."""
        # Create organization and user
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="writer@example.com",
            name="Writer User",
            role=UserRole.WRITER
        )
        user = await user_service.create_user(user_data, str(organization.id))
        
        # Create a note
        note_data = NoteCreate(
            title="Test Note",
            content="This is a test note content"
        )
        note = await note_service.create_note(note_data, str(organization.id), str(user.id))
        
        assert note.title == "Test Note"
        assert note.content == "This is a test note content"
        assert note.organization_id == organization.id
        assert note.created_by == user.id
        assert note.id is not None
    
    async def test_get_note_by_id(self, note_service, user_service, organization_service):
        """Test retrieving note by ID."""
        # Create organization, user, and note
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="writer@example.com",
            name="Writer User",
            role=UserRole.WRITER
        )
        user = await user_service.create_user(user_data, str(organization.id))
        
        note_data = NoteCreate(
            title="Test Note",
            content="This is a test note content"
        )
        created_note = await note_service.create_note(note_data, str(organization.id), str(user.id))
        
        # Retrieve note
        retrieved_note = await note_service.get_note_by_id(str(created_note.id))
        
        assert retrieved_note is not None
        assert retrieved_note.id == created_note.id
        assert retrieved_note.title == created_note.title
    
    async def test_get_notes_by_organization(self, note_service, user_service, organization_service):
        """Test retrieving all notes in an organization."""
        # Create organization and user
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="writer@example.com",
            name="Writer User",
            role=UserRole.WRITER
        )
        user = await user_service.create_user(user_data, str(organization.id))
        
        # Create multiple notes
        notes_data = [
            NoteCreate(title="Note 1", content="Content 1"),
            NoteCreate(title="Note 2", content="Content 2"),
            NoteCreate(title="Note 3", content="Content 3"),
        ]
        
        for note_data in notes_data:
            await note_service.create_note(note_data, str(organization.id), str(user.id))
        
        # Retrieve all notes
        notes = await note_service.get_notes_by_organization(str(organization.id))
        
        assert len(notes) == 3
        titles = [note.title for note in notes]
        assert "Note 1" in titles
        assert "Note 2" in titles
        assert "Note 3" in titles
    
    async def test_delete_note(self, note_service, user_service, organization_service):
        """Test deleting a note."""
        # Create organization, user, and note
        org_data = OrganizationCreate(name="Test Organization")
        organization = await organization_service.create_organization(org_data)
        
        user_data = UserCreate(
            email="writer@example.com",
            name="Writer User",
            role=UserRole.WRITER
        )
        user = await user_service.create_user(user_data, str(organization.id))
        
        note_data = NoteCreate(
            title="Test Note",
            content="This is a test note content"
        )
        created_note = await note_service.create_note(note_data, str(organization.id), str(user.id))
        
        # Delete note
        deleted = await note_service.delete_note(str(created_note.id))
        assert deleted is True
        
        # Verify note is deleted
        retrieved_note = await note_service.get_note_by_id(str(created_note.id))
        assert retrieved_note is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
