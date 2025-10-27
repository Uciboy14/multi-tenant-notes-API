# Multi-Tenant Notes API with Role-Based Access Control

A professional FastAPI application implementing a multi-tenant Notes API with strict role-based access control, built for BlueTech Interview Test.

## 🚀 Features

- **Multi-Tenant Architecture**: Complete tenant isolation using organizations
- **Role-Based Access Control**: Three-tier permission system (reader, writer, admin)
- **Async MongoDB Integration**: High-performance async database operations
- **Comprehensive API**: Full CRUD operations for organizations, users, and notes
- **Professional Architecture**: Clean separation of concerns with services, models, and API layers
- **Authentication Middleware**: Header-based authentication with tenant validation
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Docker Support**: Complete containerization with docker-compose
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 🏗️ ArchitectureMulti-Tenant Notes API

```
app/
├── api/                    # API route handlers
│   ├── organizations.py   # Organization endpoints
│   ├── users.py          # User management endpoints
│   └── notes.py          # Notes CRUD endpoints
├── core/                  # Core application components
│   ├── auth.py           # Authentication and RBAC
│   ├── config.py         # Configuration management
│   └── database.py       # Database connection
├── models/                # Pydantic data models
│   └── schemas.py        # Request/response schemas
├── services/              # Business logic layer
│   └── __init__.py       # Service classes
|   ├── note_service.py    # Note service
│   ├── organization_service.py # Organization service
│   └── user_service.py # User service
│
└── main.py               # FastAPI application
```

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor async driver
- **Pydantic**: Data validation and serialization
- **Motor**: Async MongoDB driver
- **Pytest**: Testing framework with async support
- **Docker**: Containerization and orchestration

## 📋 Prerequisites

- Python 3.11+
- MongoDB 7.0+
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd BlueTech_Interview_Test
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Option 2: Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=password \
     mongo:7.0

   # Or install MongoDB locally
   ```

3. **Set environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 API Documentation

### Authentication

All API requests require authentication headers:
- `X-Org-ID`: Organization ID (MongoDB ObjectId)
- `X-User-ID`: User ID (MongoDB ObjectId)

### Role-Based Permissions

| Role   | Organizations | Users | Notes (Read) | Notes (Write) | Notes (Delete) |
|--------|---------------|-------|--------------|---------------|----------------|
| Reader | ❌            | ❌    | ✅           | ❌            | ❌             |
| Writer | ❌            | ❌    | ✅           | ✅            | ❌             |
| Admin  | ✅            | ✅    | ✅           | ✅            | ✅             |

## 🔗 API Endpoints

### Organizations

#### Create Organization
```bash
POST /organizations/
Content-Type: application/json

{
  "name": "Acme Corporation"
}
```

#### Get Organization
```bash
GET /organizations/{org_id}
```

### Users

#### Create User
```bash
POST /organizations/{org_id}/users/
Content-Type: application/json
X-Org-ID: {org_id}
X-User-ID: {admin_user_id}

{
  "email": "john@acme.com",
  "name": "John Doe",
  "role": "writer"
}
```

#### Get Users
```bash
GET /organizations/{org_id}/users/
X-Org-ID: {org_id}
X-User-ID: {admin_user_id}
```

### Notes

#### Create Note
```bash
POST /notes/
Content-Type: application/json
X-Org-ID: {org_id}
X-User-ID: {user_id}

{
  "title": "Project Planning",
  "content": "Meeting notes for Q1 planning session..."
}
```

#### Get Notes
```bash
GET /notes/
X-Org-ID: {org_id}
X-User-ID: {user_id}
```

#### Get Specific Note
```bash
GET /notes/{note_id}
X-Org-ID: {org_id}
X-User-ID: {user_id}
```

#### Update Note
```bash
PUT /notes/{note_id}
Content-Type: application/json
X-Org-ID: {org_id}
X-User-ID: {user_id}

{
  "title": "Updated Project Planning",
  "content": "Updated meeting notes..."
}
```

#### Delete Note
```bash
DELETE /notes/{note_id}
X-Org-ID: {org_id}
X-User-ID: {admin_user_id}
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=app
```

### Test Structure

- **Unit Tests**: Test individual service methods
- **Integration Tests**: Test API endpoints and workflows
- **Permission Tests**: Verify role-based access control
- **Tenant Isolation Tests**: Ensure proper data separation

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://admin:password@localhost:27017/notes_api?authSource=admin` |
| `DATABASE_NAME` | Database name | `notes_api` |
| `APP_NAME` | Application name | `Multi-Tenant Notes API` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |

### Database Schema

#### Organizations Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "created_at": "datetime"
}
```

#### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string",
  "role": "reader|writer|admin",
  "organization_id": "ObjectId",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Notes Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string",
  "organization_id": "ObjectId",
  "created_by": "ObjectId",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🚀 Example Workflow

### 1. Create Organization
```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corporation"}'
```

### 2. Create Admin User
```bash
curl -X POST "http://localhost:8000/organizations/{org_id}/users/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {admin_user_id}" \
  -d '{
    "email": "admin@acme.com",
    "name": "Admin User",
    "role": "admin"
  }'
```

### 3. Create Writer User
```bash
curl -X POST "http://localhost:8000/organizations/{org_id}/users/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {admin_user_id}" \
  -d '{
    "email": "writer@acme.com",
    "name": "Writer User",
    "role": "writer"
  }'
```

### 4. Create Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {writer_user_id}" \
  -d '{
    "title": "Project Planning",
    "content": "Meeting notes for Q1 planning session..."
  }'
```

### 5. Retrieve Notes
```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {user_id}"
```

## 🔒 Security Features

- **Tenant Isolation**: Complete data separation between organizations
- **Role-Based Access Control**: Granular permissions based on user roles
- **Input Validation**: Comprehensive data validation with Pydantic
- **Error Handling**: Secure error responses without information leakage
- **Header Authentication**: Simple but effective authentication mechanism

## 📈 Performance Features

- **Async Operations**: Non-blocking database operations with Motor
- **Connection Pooling**: Efficient MongoDB connection management
- **Indexed Queries**: Optimized database indexes for common operations
- **Pagination Support**: Efficient handling of large datasets

## 🐳 Docker Deployment

### Production Deployment

1. **Build production image:**
   ```bash
   docker build -t notes-api:latest .
   ```

2. **Run with production settings:**
   ```bash
   docker run -d \
     --name notes-api \
     -p 8000:8000 \
     -e ENVIRONMENT=production \
     -e DEBUG=false \
     -e MONGODB_URL=mongodb://admin:password@mongodb:27017/notes_api?authSource=admin \
     notes-api:latest
   ```

### Docker Compose for Production

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongodb_data:/data/db

  api:
    build: .
    environment:
      MONGODB_URL: mongodb://admin:${MONGO_PASSWORD}@mongodb:27017/notes_api?authSource=admin
      ENVIRONMENT: production
      DEBUG: false
    depends_on:
      - mongodb

volumes:
  mongodb_data:
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is created for BlueTech Interview Test purposes.

## 🆘 Support

For questions or issues, please refer to the API documentation at `/docs` or contact the development team.

---

**Built with ❤️ using FastAPI, MongoDB, and modern Python practices.**
