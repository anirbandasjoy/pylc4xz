#!/bin/bash
# Complete User Management Script
# This script registers an admin user and allows role updates

set -e

BASE_URL="http://localhost:8000/api/v1"

echo "============================================================"
echo "🗄️  FastAPI User Management Tool"
echo "============================================================"
echo ""

# Function to register admin
register_admin() {
    echo "📝 Registering new admin user..."
    echo ""

    read -p "Email: " email
    read -p "Username: " username
    read -sp "Password (min 6 chars): " password
    echo ""
    read -p "First Name: " first_name
    read -p "Last Name: " last_name

    response=$(curl -s -X POST "$BASE_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$email\",
            \"username\": \"$username\",
            \"password\": \"$password\",
            \"first_name\": \"$first_name\",
            \"last_name\": \"$last_name\"
        }")

    echo ""
    echo "$response" | python3 -m json.tool

    # Check if registration was successful
    if echo "$response" | grep -q "\"role\": \"admin\""; then
        echo ""
        echo "✅ Admin user registered successfully!"
        echo "   Role: admin"
        echo "   Verified: true"
    else
        echo ""
        echo "⚠️  User registered but may not be admin (if not first user)"
    fi
}

# Function to login
login_user() {
    echo "🔐 Logging in..."
    echo ""

    read -p "Username or Email: " username
    read -sp "Password: " password
    echo ""

    response=$(curl -s -X POST "$BASE_URL/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$username&password=$password")

    echo "$response" | python3 -m json.tool

    # Extract access token
    ACCESS_TOKEN=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

    if [ -n "$ACCESS_TOKEN" ]; then
        echo ""
        echo "✅ Login successful!"
        echo "   Access Token: ${ACCESS_TOKEN:0:50}..."
        echo ""
        echo "💾 Save this token for API calls:"
        echo "   export TOKEN='$ACCESS_TOKEN'"
    fi
}

# Function to list all users
list_users() {
    echo "👥 Listing all users..."
    echo ""

    if [ -z "$TOKEN" ]; then
        read -p "Enter admin token: " TOKEN
    fi

    response=$(curl -s -X GET "$BASE_URL/users/?skip=0&limit=100" \
        -H "Authorization: Bearer $TOKEN")

    echo "$response" | python3 -m json.tool
}

# Function to update user role
update_role() {
    echo "🔄 Updating user role..."
    echo ""

    if [ -z "$TOKEN" ]; then
        read -p "Enter admin token: " TOKEN
    fi

    read -p "Enter User ID to update: " user_id
    echo "Available roles: admin, moderator, user"
    read -p "Enter new role: " new_role

    response=$(curl -s -X PUT "$BASE_URL/users/$user_id" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "{\"role\": \"$new_role\"}")

    echo ""
    echo "$response" | python3 -m json.tool
    echo ""
    echo "✅ User role updated!"
}

# Function to activate/deactivate user
toggle_user() {
    echo "⚡ Toggling user status..."
    echo ""

    if [ -z "$TOKEN" ]; then
        read -p "Enter admin token: " TOKEN
    fi

    read -p "Enter User ID: " user_id
    echo "1. Activate user"
    echo "2. Deactivate user"
    read -p "Choose action: " action

    if [ "$action" == "1" ]; then
        endpoint="activate"
    else
        endpoint="deactivate"
    fi

    response=$(curl -s -X PATCH "$BASE_URL/users/$user_id/$endpoint" \
        -H "Authorization: Bearer $TOKEN")

    echo ""
    echo "$response" | python3 -m json.tool
}

# Function to verify user
verify_user() {
    echo "✅ Verifying user..."
    echo ""

    if [ -z "$TOKEN" ]; then
        read -p "Enter admin token: " TOKEN
    fi

    read -p "Enter User ID to verify: " user_id

    response=$(curl -s -X PATCH "$BASE_URL/users/$user_id/verify" \
        -H "Authorization: Bearer $TOKEN")

    echo ""
    echo "$response" | python3 -m json.tool
}

# Main menu
show_menu() {
    echo ""
    echo "============================================================"
    echo "Main Menu"
    echo "============================================================"
    echo "1. Register Admin User"
    echo "2. Login"
    echo "3. List All Users"
    echo "4. Update User Role"
    echo "5. Activate/Deactivate User"
    echo "6. Verify User"
    echo "7. Exit"
    echo ""
    read -p "Choose an option: " choice

    case $choice in
        1) register_admin ;;
        2) login_user ;;
        3) list_users ;;
        4) update_role ;;
        5) toggle_user ;;
        6) verify_user ;;
        7) echo "👋 Goodbye!"; exit 0 ;;
        *) echo "❌ Invalid option!"; sleep 1 ;;
    esac
}

# Main loop
while true; do
    show_menu
done
