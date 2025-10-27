# Complete Usage Guide - Multi-Tenant Notes API

## 🎯 Overview

This API uses **custom headers** for authentication. You must include these headers in all requests that require authentication.

**Required Headers:**
- `X-Org-ID`: Your organization ID (MongoDB ObjectId)
- `X-User-ID`: Your user ID (MongoDB ObjectId)

## 📍 Quick Links

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Root Endpoint:** http://localhost:8000/

---

## 🚀 Getting Started - Step by Step

### Step 1: Start the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Create Your Organization

**Note:** Organization creation does NOT require headers.

```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Company"}'
```

**Response:**
```json
{
  "name": "My Company",
  "_id": "68ff5262e96cd1b2a9781e8a",
  "created_at": "2025-10-27T11:07:14.173000"
}
```

**Save the `_id` value as `ORG_ID`** (e.g., `68ff5262e96cd1b2a9781e8a`)

### Step 3: View Your Organization

```bash
curl -X GET "http://localhost:8000/organizations/68ff5262e96cd1b2a9781e8a"
```

---

## ⚠️ **HOW TO GET YOUR USER_ID**

Currently, you need to create a user to get a user_id. However, to create a user you need an existing user (chicken and egg problem).

**Solution:** The current implementation requires you to manually create a user in the database OR use a temporary approach.

### Option A: Use Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Find "POST /organizations/{org_id}/users/"
3. Click "Try it out"
4. Enter your ORG_ID
5. **For now, just enter any valid ObjectId format** (e.g., `507f1f77bcf86cd799439011`) for X-Org-ID and X-User-ID
6. Submit the request
7. You'll get a user created
8. **Copy the `_id` from response** - this is your USER_ID

### Option B: Manual Database Creation

```bash
# Connect to MongoDB
mongosh

# Switch to your database
use notes_api

# Insert a user manually
db.users.insertOne({
  "email": "admin@mycompany.com",
  "name": "Admin User",
  "role": "admin",
  "organization_id": ObjectId("YOUR_ORG_ID_HERE"),
  "created_at": new Date()
})
```

Copy the returned `_id` - this is your USER_ID.

---

## 📝 Using the Headers

Once you have `ORG_ID` and `USER_ID`, use them like this:

```bash
# Example: Create a note
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: 68ff5262e96cd1b2a9781e8a" \
  -H "X-User-ID: YOUR_USER_ID" \
  -d '{
    "title": "My First Note",
    "content": "This is a test note"
  }'
```

---

## 🎯 Why Custom Headers?

Custom headers like `X-Org-ID` and `X-User-ID` are used because:

1. **Simplicity:** No complex token management
2. **Direct:** Works well for multi-tenant apps
3. **Fast:** No token validation overhead
4. **Clear:** Headers explicitly show which tenant/user you're acting as

**Note:** In production, you'd typically use JWT tokens that contain this information, but this header-based approach is valid for many use cases.

---

## 🔐 Understanding Authentication

### How It Works:

1. **Middleware** (automatically runs): Extracts headers from every request
2. **Validation**: Checks if headers are valid ObjectIds
3. **Database Lookup**: Verifies user exists and belongs to the organization
4. **Access Control**: Applies role-based permissions

### What Headers Do:

```
X-Org-ID: Which organization/tenant you're acting as
X-User-ID: Which user you're authenticated as

Together, they form your identity in the system.
```

---

## 🧪 Testing in Swagger UI

1. **Open:** http://localhost:8000/docs
2. **Try an endpoint** (e.g., "GET /notes/")
3. **Click "Try it out"**
4. **You'll see:** Fields for X-Org-ID and X-User-ID
5. **Enter your IDs**
6. **Click "Execute"**

This visual interface makes it easy to test without curl!

---

## 📋 Common Workflows

### Workflow 1: Create Organization & First User

```bash
# 1. Create organization
ORG_RESPONSE=$(curl -s -X POST http://localhost:8000/organizations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp"}')

ORG_ID=$(echo $ORG_RESPONSE | grep -o '"_id":"[^"]*"' | cut -d'"' -f4)

echo "Organization created: $ORG_ID"

# 2. Get your user ID from database or create manually
# For now, let's just test without a real user
TEMP_USER_ID="507f1f77bcf86cd799439011"

# 3. Create note
curl -X POST http://localhost:8000/notes/ \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: $ORG_ID" \
  -H "X-User-ID: $TEMP_USER_ID" \
  -d '{"title": "Test", "content": "Test content"}'
```

---

## ❓ FAQ

### Q: Where do I put the headers in API docs?

**A:** In Swagger UI (/docs), when you click "Try it out" on any endpoint, you'll see input fields for X-Org-ID and X-User-ID at the top. These are automatically added by FastAPI.

### Q: How do I generate org_id and user_id dynamically?

**A:** Currently they're created when you:
- Create an organization → gives you org_id
- Create a user → gives you user_id

For JWT-based dynamic generation, see the JWT implementation section.

### Q: Why do I need both headers?

**A:** 
- `X-Org-ID`: Identifies which tenant/organization
- `X-User-ID`: Identifies which user (and their role/permissions)

Together they ensure multi-tenancy and security.

### Q: Can I skip the headers?

**A:** Only for:
- `/organizations/` endpoints (public)
- `/health`, `/`, `/docs` (public)

All other endpoints require both headers.

---

## 🔧 Troubleshooting

### Error: "Missing required headers"

**Solution:** You forgot to include X-Org-ID and/or X-User-ID in your request.

### Error: "Invalid organization or user ID format"

**Solution:** Make sure your IDs are valid MongoDB ObjectId format (24 hex characters).

### Error: "User not found"

**Solution:** The user_id you're using doesn't exist. Create a user first or use a valid ID.

---

## 📞 Need Help?

- Check the interactive docs: http://localhost:8000/docs
- Review the test script: `bash test_complete_api.sh`
- See detailed examples in `QUICK_START.md`

