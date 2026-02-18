#!/bin/bash
# Update User Role Script
# Usage: ./update_user_role.sh <user_id> <new_role> <admin_token>

USER_ID=$1
NEW_ROLE=$2
TOKEN=$3

if [ -z "$USER_ID" ] || [ -z "$NEW_ROLE" ] || [ -z "$TOKEN" ]; then
    echo "❌ Usage: $0 <user_id> <new_role> <admin_token>"
    echo ""
    echo "Available roles: admin, moderator, user"
    echo ""
    echo "Example:"
    echo "  $0 2 moderator eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    exit 1
fi

echo "🔄 Updating user role..."
echo "   User ID: $USER_ID"
echo "   New Role: $NEW_ROLE"
echo ""

response=$(curl -s -X PUT "http://localhost:8000/api/v1/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"role\": \"$NEW_ROLE\"}")

echo "$response" | python3 -m json.tool

echo ""
echo "✅ Done!"
