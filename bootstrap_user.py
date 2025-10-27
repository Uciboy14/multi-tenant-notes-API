#!/usr/bin/env python3
"""Helper script to bootstrap the first admin user for an organization."""

import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId

# Database configuration
MONGO_URL = "mongodb://localhost:27017/notes_api"
DB_NAME = "notes_api"

async def bootstrap_user(org_id: str, email: str, name: str, role: str = "admin"):
    """Create the first admin user for an organization."""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Check if org exists
        org = await db.organizations.find_one({"_id": ObjectId(org_id)})
        if not org:
            print(f"❌ Organization {org_id} not found")
            return False
        
        print(f"✅ Found organization: {org['name']}")
        
        # Check if any users exist
        existing = await db.users.count_documents({"organization_id": ObjectId(org_id)})
        if existing > 0:
            print(f"⚠️  Organization already has {existing} user(s)")
            # Ask if they want to continue
            response = input("Create user anyway? (yes/no): ")
            if response.lower() != 'yes':
                return False
        
        # Create user
        user_doc = {
            "email": email,
            "name": name,
            "role": role,
            "organization_id": ObjectId(org_id),
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_doc)
        user_id = result.inserted_id
        
        print(f"✅ Created user: {email}")
        print(f"📝 User ID: {user_id}")
        print(f"🏢 Organization ID: {org_id}")
        print(f"\nNow you can use these headers:")
        print(f"  X-Org-ID: {org_id}")
        print(f"  X-User-ID: {user_id}")
        
        # Close connection
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    if len(sys.argv) < 4:
        print("Usage: python bootstrap_user.py <org_id> <email> <name> [role]")
        print("\nExample:")
        print("  python bootstrap_user.py 68ff5262e96cd1b2a9781e8a admin@test.com 'Admin User' admin")
        sys.exit(1)
    
    org_id = sys.argv[1]
    email = sys.argv[2]
    name = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else "admin"
    
    await bootstrap_user(org_id, email, name, role)

if __name__ == "__main__":
    asyncio.run(main())

