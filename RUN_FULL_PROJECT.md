# 🚀 Full Project Setup Guide - Interactive Mode

## Step-by-Step Instructions to Run the Complete Project

### Step 1: Clean Up Any Existing Containers

```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers (optional, if you want a clean start)
docker rm $(docker ps -aq)

# Or use the cleanup script
make clean  # or ./cleanup.sh
```

### Step 2: Start PostgreSQL in Interactive Mode

```bash
# Start PostgreSQL in foreground (you'll see logs)
docker-compose up

# Press Ctrl+C to stop
```

**First time?** You'll see PostgreSQL download and initialize. Wait for this message:
```
fastapi_postgres  | database system is ready to accept connections
```

### Step 3: Open a New Terminal for the Application

Keep PostgreSQL running in the first terminal. Open a new terminal:

```bash
# Navigate to project
cd ~/Documents/personal/fastApi

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run FastAPI in interactive mode
uvicorn main:app --reload
```

### Step 4: Access Your Application

Once both are running:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

---

## 📋 Complete Quick Start (All Commands)

```bash
# Terminal 1: PostgreSQL
docker-compose up

# Terminal 2: FastAPI Application
cd ~/Documents/personal/fastApi
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

---

## 🛠️ Useful Commands

### PostgreSQL Management

```bash
# Start in foreground (interactive)
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f postgres

# Stop all
docker-compose down

# Stop and delete all data
docker-compose down -v
```

### Database Shell Access

```bash
# Access PostgreSQL shell inside container
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db

# List all tables
\dt

# List all users
SELECT id, email, username, role, is_active FROM users;

# Exit
\q
```

### Application Management

```bash
# Run with auto-reload (development)
uvicorn main:app --reload

# Run without reload (production)
uvicorn main:app

# Run on specific port
uvicorn main:app --port 8080

# Run with specific host
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔍 Troubleshooting

### Port 5432 Already in Use?

```bash
# Check what's using the port
sudo lsof -i :5432

# Stop local PostgreSQL
sudo service postgresql stop

# OR use alternative port
docker-compose -f docker-compose-alt-port.yml up
```

### Database Connection Error?

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test database connection
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT 1;"
```

### Tables Not Created?

The application automatically creates tables on startup. Check:
```bash
# Look for this in startup logs:
# "Creating database tables..."
# "Database initialized!"
```

### Permission Issues?

```bash
# Fix script permissions
chmod +x start.sh
chmod +x start-alt-port.sh
chmod +x check-ports.sh
```

---

## 📊 Project Structure Overview

```
Terminal 1 (Docker)          Terminal 2 (FastAPI)
┌──────────────────┐        ┌──────────────────┐
│  PostgreSQL      │◄──────►│  FastAPI App     │
│  Port: 5432      │        │  Port: 8000      │
│  Container       │        │  Virtual Env     │
└──────────────────┘        └──────────────────┘
        │                            │
        └────────┬───────────────────┘
                 ▼
         ┌──────────────┐
         │  pgAdmin     │
         │  Port: 5050  │
         └──────────────┘
```

---

## 🎯 Common Workflows

### Development Workflow

1. **Start PostgreSQL**: `docker-compose up` (Terminal 1)
2. **Start FastAPI**: `uvicorn main:app --reload` (Terminal 2)
3. **Code changes**: FastAPI auto-reloads
4. **View logs**: Both terminals show real-time logs
5. **Stop**: Press Ctrl+C in both terminals

### Testing Authentication

```bash
# 1. Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=Test123!"

# 3. Access protected route (use token from step 2)
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove virtual environment
rm -rf venv

# Remove .env file
rm .env

# Start fresh
docker-compose up
```

---

## 📚 Quick Reference

| Command | Purpose |
|---------|---------|
| `docker-compose up` | Start PostgreSQL in foreground |
| `docker-compose up -d` | Start PostgreSQL in background |
| `docker-compose down` | Stop PostgreSQL |
| `docker-compose logs -f postgres` | Follow PostgreSQL logs |
| `docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db` | Database shell |
| `uvicorn main:app --reload` | Run FastAPI with auto-reload |
| `source venv/bin/activate` | Activate virtual environment |
| `pip install -r requirements.txt` | Install dependencies |

---

## ✅ Check if Everything is Working

```bash
# 1. Check PostgreSQL is running
docker ps | grep postgres

# 2. Check database is accessible
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"

# 3. Check FastAPI is running
curl http://localhost:8000/health

# 4. Check API docs
curl http://localhost:8000/docs
# Open in browser: http://localhost:8000/docs
```

---

## 🎓 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Register User**: Create your first user account
3. **Test Authentication**: Login and get JWT token
4. **Explore pgAdmin**: Visit http://localhost:5050 to manage database
5. **Build Features**: Start adding your own endpoints

---

## 💡 Tips

- Keep PostgreSQL running in a separate terminal
- Use `--reload` flag for development (auto-restart on code changes)
- Check both terminals for error messages
- Use pgAdmin to visually inspect the database
- Make database changes through the API, not directly in PostgreSQL
