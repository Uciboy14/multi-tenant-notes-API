# Quick Start Guide

## 1. Start the Server

```bash
# If not already running
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 2. Test the API

### Quick Test
```bash
bash test_complete_api.sh
```

### Manual Test Flow

#### Step 1: Create Organization
```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Company"}'
```

Response:
```json
{
  "name": "My Company",
  "_id": "68ff5262e96cd1b2a9781e8a",
  "created_at": "2025-10-27T11:07:14.173000"
}
```

Save the `_id` as `ORG_ID`.

#### Step 2: Get Organization
```bash
curl -X GET "http://localhost:8000/organizations/{ORG_ID}"
```

#### Step 3: Test Middleware (should fail)
```bash
curl -X GET "http://localhost:8000/notes/"
```

Expected:
```json
{"detail": "Missing required headers: X-Org-ID and X-User-ID"}
```

## 3. Full Workflow (Next Steps)

### Create a User
```bash
curl -X POST "http://localhost:8000/organizations/{ORG_ID}/users/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {ORG_ID}" \
  -H "X-User-ID: {temp_user_id}" \
  -d '{
    "email": "admin@mycompany.com",
    "name": "Admin User",
    "role": "admin"
  }'
```

Save the returned `_id` as `USER_ID`.

### Create a Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {ORG_ID}" \
  -H "X-User-ID: {USER_ID}" \
  -d '{
    "title": "My First Note",
    "content": "This is a test note"
  }'
```

### Get Notes
```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "X-Org-ID: {ORG_ID}" \
  -H "X-User-ID: {USER_ID}"
```

## 4. Interactive Testing

Open in browser: **http://localhost:8000/docs**

This provides a full interactive UI for testing all endpoints.

## 5. Run Automated Tests

```bash
# Run all tests
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=app
```

## Features Verified

✅ Middleware automatically extracts tenant/user from headers  
✅ Blocks requests without proper headers  
✅ Public endpoints work without auth  
✅ Organizations can be created and retrieved  
✅ MongoDB integration working properly  
✅ ObjectId conversion working correctly  

