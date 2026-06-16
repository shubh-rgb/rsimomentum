# 🚀 Quick Reference Guide

## Environment Setup

```bash
# 1. Create environment file
cp .env.example .env

# 2. Edit with your credentials
nano .env

# Required values:
# POSTGRES_USER=trader
# POSTGRES_PASSWORD=your_secure_password
# DB_URL=postgresql://trader:password@localhost:5433/marketdb
```

## Installation & Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL (Docker)
docker run -d \
  --name postgres-rsi \
  -e POSTGRES_USER=trader \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=marketdb \
  -p 5433:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# 3. Initialize database
python3 -c "from database.storage import init_db; init_db()"
```

## Run the Application

```bash
# Terminal 1: Start Scheduler
python3 main.py

# Terminal 2: Start Dashboard  
streamlit run dashboard.py

# Access: http://localhost:8501
# Login: admin / admin123
```

## Docker Deployment

```bash
# All-in-one setup
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| DB connection error | Check .env file, ensure DB is running |
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| Login fails | Clear Streamlit cache: `rm -rf ~/.streamlit/` |
| Port already in use | Change port in `.streamlit/config.toml` |

## Key Files

| File | Purpose |
|------|---------|
| README.md | Full setup guide (START HERE) |
| SECURITY_FIXES.md | Security improvements |
| .env.example | Environment template |
| requirements.txt | Python dependencies |
| docker-compose.yml | Docker orchestration |
| config.py | Application config |
| dashboard.py | Web interface |
| main.py | Entry point |

## Default Credentials

```
Username: admin
Password: admin123
⚠️ CHANGE BEFORE PRODUCTION!
```

## Important Security Notes

- ✅ Never commit .env file (credentials)
- ✅ Use strong passwords
- ✅ Update default credentials
- ✅ Setup HTTPS for production
- ✅ Restrict database access
- ✅ Monitor logs regularly

## Logs & Debugging

```bash
# View application logs
tail -f logs/app.log

# Database query
psql -h localhost -p 5433 -U trader -d marketdb
SELECT * FROM scans ORDER BY scan_time DESC LIMIT 5;

# Python debugging
python3 -c "from scanner.engine import run_scan; run_scan()"
```

## Common Commands

```bash
# Database backup
docker exec postgres-rsi pg_dump -U trader marketdb > backup.sql

# Database restore
docker exec -i postgres-rsi psql -U trader marketdb < backup.sql

# Restart services
docker-compose restart

# Rebuild images
docker-compose build --no-cache

# Test configuration
python3 -c "from config import DB_URL; print(f'✅ DB_URL: {DB_URL[:20]}...')"
```

## Resources

- 📖 Full Documentation: [README.md](README.md)
- 🔐 Security Details: [SECURITY_FIXES.md](SECURITY_FIXES.md)
- 📋 GitHub Checklist: [GITHUB_PUSH_CHECKLIST.md](GITHUB_PUSH_CHECKLIST.md)
- 🐳 Docker Guide: [docker-compose.yml](docker-compose.yml)

---

**Last Updated**: June 16, 2026  
**Status**: ✅ Production Ready
