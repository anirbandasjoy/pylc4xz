# ⚡ Quick Start - Interactive Mode

## 🎯 You want to run the full project interactively? Here's how:

### Option 1: Interactive Menu (Easiest) ✨

```bash
./run-project.sh
```

This gives you a menu with all options:
- Start PostgreSQL
- Start FastAPI
- Start Both
- View Logs
- Database Shell
- Cleanup
- And more!

### Option 2: Two Terminal Method (Recommended for Development)

**Terminal 1 - Start PostgreSQL:**
```bash
docker-compose up
```
Keep this terminal open to see PostgreSQL logs.

**Terminal 2 - Start FastAPI:**
```bash
cd ~/Documents/personal/fastApi

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Create .env file (first time only)
cp .env.example .env

# Run FastAPI
uvicorn main:app --reload
```

### Option 3: Using Make Commands

```bash
# See all available commands
make help

# Start PostgreSQL in background
make start

# Run FastAPI
make run

# View logs
make logs

# Stop everything
make stop

# Interactive menu
make dev-all
```

### Option 4: Start Script (Automated)

```bash
./start.sh
```

---

## 📋 Step-by-Step for First Time Setup

### 1. Clean Everything First

```bash
# Stop and remove all containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
```

### 2. Start PostgreSQL (Terminal 1)

```bash
docker-compose up
```

**Wait for this message:**
```
fastapi_postgres  | database system is ready to accept connections
```

### 3. Setup & Start FastAPI (Terminal 2)

```bash
# Go to project directory
cd ~/Documents/personal/fastApi

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run FastAPI
uvicorn main:app --reload
```

### 4. Access Your Application

Open in browser:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **pgAdmin**: http://localhost:5050

---

## 🛠️ Common Commands

| Command | What it does |
|---------|--------------|
| `docker-compose up` | Start PostgreSQL in foreground (interactive) |
| `docker-compose up -d` | Start PostgreSQL in background |
| `docker-compose down` | Stop PostgreSQL |
| `docker-compose logs -f postgres` | Follow PostgreSQL logs |
| `make start-fg` | Start PostgreSQL in foreground |
| `make start` | Start PostgreSQL in background |
| `make run` | Run FastAPI application |
| `make logs` | Show PostgreSQL logs |
| `make status` | Check what's running |
| `./run-project.sh` | Interactive menu |

---

## 🔍 Check if Everything Works

```bash
# Check PostgreSQL
docker ps | grep postgres

# Check database connection
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT 1;"

# Check FastAPI
curl http://localhost:8000/health
```

---

## ❌ Stopping Everything

**Stop both PostgreSQL and FastAPI:**

1. Press `Ctrl+C` in FastAPI terminal
2. Press `Ctrl+C` in PostgreSQL terminal
3. Or use: `make stop`

---

## 🔄 Development Workflow

1. **Start PostgreSQL**: `docker-compose up` (Terminal 1)
2. **Start FastAPI**: `uvicorn main:app --reload` (Terminal 2)
3. **Edit code**: FastAPI auto-reloads
4. **Check logs**: Both terminals show real-time logs
5. **Stop**: Press `Ctrl+C` in both terminals

---

## 📊 Project Architecture

```
┌─────────────────────────────────────────────┐
│           Your Browser                      │
│  http://localhost:8000/docs                 │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │   FastAPI    │
│  Docker:5432 │  │  Port:8000   │
│              │◄─┤              │
└──────────────┘  └──────────────┘
       │
       ▼
┌──────────────┐
│   pgAdmin    │
│  Port:5050   │
└──────────────┘
```

---

## 💡 Tips

1. **Keep two terminals open** - one for PostgreSQL, one for FastAPI
2. **Use `--reload` flag** - FastAPI automatically restarts when you edit code
3. **Check logs** - Both terminals show error messages
4. **Use Swagger UI** - Test your API at http://localhost:8000/docs
5. **PostgreSQL logs** - Shows all database queries

---

## 🎓 Learning Path

1. **Start the project** using the interactive menu: `./run-project.sh`
2. **Register a user** via Swagger UI
3. **Login** to get JWT token
4. **Test protected endpoints** with your token
5. **Explore the code** while it's running
6. **Make changes** and watch auto-reload

---

## 🆘 Troubleshooting

**Problem: Port 5432 already in use**

```bash
# Use alternative port
./start-alt-port.sh
```

**Problem: Docker permission error**

```bash
# Add user to docker group (one-time)
sudo usermod -aG docker $USER
newgrp docker
```

**Problem: Python not found**

```bash
# Install Python 3
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Problem: Dependencies not installing**

```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📞 Help

```bash
# Show all commands
make help

# Check status
make status

# Interactive menu
./run-project.sh
```

---

**Ready to start? Run:**
```bash
./run-project.sh
```

Or manually:
```bash
# Terminal 1
docker-compose up

# Terminal 2
source venv/bin/activate
uvicorn main:app --reload
```
