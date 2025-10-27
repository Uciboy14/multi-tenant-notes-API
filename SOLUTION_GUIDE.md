# Solution Guide for Your Questions

## ✅ Issue 1: Custom Headers in Swagger Docs - FIXED

**Problem:** The X-Org-ID and X-User-ID headers don't show up in the API docs.

**Solution:** I've updated the code to use FastAPI's `Header` parameter with proper documentation. The headers will now appear in the Swagger UI.

**What changed:**
- Modified `app/core/auth.py` to use `Header(..., alias="X-Org-ID", description="...")`
- Now headers appear in `/docs` interface with proper descriptions

## 🔄 Issue 2: JWT Token Implementation - NEEDS IMPLEMENTATION

**Problem:** You want to use JWT tokens to dynamically generate org_id and user_id instead of hardcoding them.

**Current Status:** Headers are passed manually.

**What needs to be done:**
1. Create JWT token generation endpoint (login)
2. Token should contain: org_id, user_id, role
3. Client sends token in Authorization header
4. Middleware extracts org_id and user_id from JWT token
5. Current header-based auth remains for backward compatibility

**Would you like me to:**
- A) Implement JWT authentication (replace current system)
- B) Add JWT as an additional auth method (keep headers as fallback)
- C) Just document how to manually create org_id and user_id for now

## 📝 Issue 3: README Update - IN PROGRESS

**What needs updating:**
1. ✅ Environment setup instructions (already good)
2. ⚠️ Step-by-step workflow showing how to:
   - Create an organization
   - Get organization ID from response
   - Use that ID to create users
   - Use IDs as headers for notes
3. Show actual curl examples with real responses
4. Add troubleshooting section

## 🧪 Issue 4: Pytest Errors - PARTIALLY FIXED

**Problem:** Test database connection uses wrong credentials.

**Fixed:** Changed test database URL from authenticated to non-auth connection.

**Remaining issues:**
- Some tests may need updates for new middleware
- Need to mock database properly
- Test fixtures may need adjustment

---

## Quick Actions You Can Take Now

### To Test Custom Headers in Swagger:
1. Start server: `uvicorn app.main:app --reload`
2. Open: http://localhost:8000/docs
3. Try any endpoint that requires auth (e.g., GET /notes/)
4. You should see "X-Org-ID" and "X-User-ID" fields at the top

### To Test the API Manually:
```bash
# 1. Create org
curl -X POST http://localhost:8000/organizations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "My Company"}'

# 2. Note the _id from response (e.g., "68ff5262e96cd1b2a9781e8a")
# 3. Save as ORG_ID

# 4. Use that ID as header
curl -X GET http://localhost:8000/notes/ \
  -H "X-Org-ID: YOUR_ORG_ID" \
  -H "X-User-ID: A_USER_ID"

# 5. See error about user not existing - this is expected!
# You need to create a user first via the /organizations/{org_id}/users/ endpoint
```

---

## Decision Needed for JWT

Would you like me to implement JWT authentication? This would allow:
- Users to "login" and get a token
- Token automatically provides org_id and user_id
- No need to manually track IDs

**Yes/No?** Or would you prefer to keep the current header-based approach documented?

