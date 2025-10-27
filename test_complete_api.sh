#!/bin/bash
# Complete API Testing Script

echo "🧪 Testing Multi-Tenant Notes API"
echo "=================================="
echo ""

# Step 1: Create an organization
echo "1️⃣ Creating an organization..."
ORG_RESPONSE=$(curl -s -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Organization '$(date +%s)'"}')

echo "Organization created: $ORG_RESPONSE"
echo ""

# Extract organization ID
ORG_ID=$(echo $ORG_RESPONSE | grep -o '"_id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$ORG_ID" ]; then
  echo "❌ Failed to get organization ID. Exiting."
  exit 1
fi

echo "Organization ID: $ORG_ID"
echo ""

# Step 2: Get the organization by ID
echo "2️⃣ Retrieving the organization..."
curl -s -X GET "http://localhost:8000/organizations/$ORG_ID" | python -m json.tool
echo ""

# Step 3: Test middleware - try to access notes without headers
echo "3️⃣ Testing middleware (should fail without headers)..."
MISSING_HEADERS=$(curl -s -X GET "http://localhost:8000/notes/")
echo "Response: $MISSING_HEADERS"
echo ""

# Step 4: Show summary
echo "✅ API Testing Complete!"
echo ""
echo "🌐 Interactive Docs: http://localhost:8000/docs"
echo "💊 Health Check: http://localhost:8000/health"
echo ""
echo "📝 Next steps:"
echo "   - Create users at POST /organizations/{org_id}/users/"
echo "   - Create notes at POST /notes/"
echo "   - Test role-based access control"
echo ""

