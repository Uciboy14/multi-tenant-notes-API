# 🚀 Quick Start Guide

## Prerequisites
- Python 3.11+
- MongoDB (or Docker for MongoDB)

## Step 1: Activate Virtual Environment
```bash
source venv/bin/activate
```

## Step 2: Start MongoDB

### Option A: Docker (if available)
```bash
docker run -d -p 27017:27017 --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:7.0
```

### Option B: Install MongoDB locally
Visit: https://www.mongodb.com/docs/manual/installation/

### Option C: Use MongoDB Atlas (free cloud)
1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `.env` file with connection string

## Step 3: Run the Application
```bash
uvicorn app.main:app --reload
```

## Step 4: Access the API
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Example Usage

### Create Organization
```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corporation"}'
```

### Create User (Admin only)
```bash
curl -X POST "http://localhost:8000/organizations/{org_id}/users/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {user_id}" \
  -d '{
    "email": "admin@acme.com",
    "name": "Admin User",
    "role": "admin"
  }'
```

### Create Note (Writer/Admin)
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {user_id}" \
  -d '{
    "title": "Project Planning",
    "content": "Meeting notes for Q1 planning..."
  }'
```

For more details, see README.md
