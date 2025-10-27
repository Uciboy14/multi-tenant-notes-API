// MongoDB initialization script
db = db.getSiblingDB('notes_api');

// Create collections with validation
db.createCollection('organizations', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'created_at'],
      properties: {
        name: {
          bsonType: 'string',
          description: 'Organization name is required and must be a string'
        },
        created_at: {
          bsonType: 'date',
          description: 'Created date is required'
        }
      }
    }
  }
});

db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'role', 'organization_id', 'created_at'],
      properties: {
        email: {
          bsonType: 'string',
          description: 'Email is required and must be a string'
        },
        role: {
          enum: ['reader', 'writer', 'admin'],
          description: 'Role must be one of: reader, writer, admin'
        },
        organization_id: {
          bsonType: 'objectId',
          description: 'Organization ID is required'
        },
        created_at: {
          bsonType: 'date',
          description: 'Created date is required'
        }
      }
    }
  }
});

db.createCollection('notes', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'content', 'organization_id', 'created_by', 'created_at'],
      properties: {
        title: {
          bsonType: 'string',
          description: 'Title is required and must be a string'
        },
        content: {
          bsonType: 'string',
          description: 'Content is required and must be a string'
        },
        organization_id: {
          bsonType: 'objectId',
          description: 'Organization ID is required'
        },
        created_by: {
          bsonType: 'objectId',
          description: 'Created by user ID is required'
        },
        created_at: {
          bsonType: 'date',
          description: 'Created date is required'
        }
      }
    }
  }
});

// Create indexes for better performance
db.organizations.createIndex({ 'name': 1 }, { unique: true });
db.users.createIndex({ 'email': 1, 'organization_id': 1 }, { unique: true });
db.users.createIndex({ 'organization_id': 1 });
db.notes.createIndex({ 'organization_id': 1 });
db.notes.createIndex({ 'created_by': 1 });
db.notes.createIndex({ 'created_at': -1 });

print('Database initialized successfully!');
