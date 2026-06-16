# Docker Compose Setup Guide

Complete steps to build, run, and manage the RSI Momentum application using Docker Compose.

---

## Prerequisites

1. **Docker Desktop** installed  
   - macOS/Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: `sudo apt-get install docker.io docker-compose`

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Check Docker daemon is running**
   ```bash
   docker ps
   ```

---

## Environment Setup

### 1. Create `.env` file in project root

```bash
cp .env.example .env  # or create manually
```

### 2. Add required variables to `.env`

```env
# PostgreSQL Configuration
POSTGRES_USER=trader
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=marketdb
DB_PORT=5433

# Database URL (used by application)
DB_URL=postgresql://trader:your_secure_password_here@db:5432/marketdb

# Kite API (if applicable)
KITE_API_KEY=your_kite_api_key
KITE_API_SECRET=your_kite_api_secret
```

**Important:** Never commit `.env` to Git. It's already in `.gitignore`.

---

## Running the Application

### 1. Start all services

```bash
docker-compose up
```

**Output should show:**
- PostgreSQL database starting and health checks
- Scanner service building and running
- Dashboard (Streamlit) accessible at http://localhost:8501

### 2. Run in background (detached mode)

```bash
docker-compose up -d
```

Check running containers:
```bash
docker-compose ps
```

### 3. View logs

All services:
```bash
docker-compose logs -f
```

Specific service:
```bash
docker-compose logs -f db
docker-compose logs -f scanner
docker-compose logs -f dashboard
```

---

## Service Details

### PostgreSQL Database (`db`)
- **Image:** postgres:16
- **Port:** 5433 (external) → 5432 (container)
- **Volume:** `pgdata:/var/lib/postgresql/data` (persistent data)
- **Health Check:** Checks every 5s, fails after 50s (10 retries × 5s)
- **Restart Policy:** Always restart if crashed

**Connect directly (local development):**
```bash
psql -h localhost -p 5433 -U trader -d marketdb
# Password: (from .env POSTGRES_PASSWORD)
```

### Scanner Service (`scanner`)
- **Command:** `python main.py`
- **Depends On:** Database (waits for health check)
- **Environment:** Reads `DB_URL` from `.env`
- **Logs:** Mounted at `./logs:/app/logs`
- **Restart Policy:** Always restart if crashed

### Dashboard Service (`dashboard`)
- **Type:** Streamlit web UI
- **Port:** 8501 (accessible at http://localhost:8501)
- **Command:** `streamlit run dashboard.py`
- **Depends On:** Database (waits for health check)
- **Restart Policy:** Always restart if crashed

---

## Common Commands

### Build images (force rebuild)
```bash
docker-compose build --no-cache
```

### Rebuild and start
```bash
docker-compose up --build
```

### Stop all services
```bash
docker-compose stop
```

### Stop and remove containers (keep volumes)
```bash
docker-compose down
```

### Stop, remove containers, AND remove volumes
```bash
docker-compose down -v
```

### Remove all images built by compose
```bash
docker-compose down --rmi all
```

### Access shell in running container
```bash
docker-compose exec scanner bash
docker-compose exec dashboard bash
docker-compose exec db psql -U trader -d marketdb
```

### Restart a single service
```bash
docker-compose restart scanner
docker-compose restart dashboard
```

### Check resource usage
```bash
docker stats
```

---

## Verification Checklist

After running `docker-compose up`:

- [ ] Database is healthy (logs show "database system is ready to accept connections")
- [ ] Scanner started without errors (logs show main.py running)
- [ ] Dashboard is accessible at http://localhost:8501
- [ ] Database persists data in `pgdata` volume
- [ ] Logs are written to `./logs` directory

**Test database connection:**
```bash
docker-compose exec db psql -U trader -d marketdb -c "SELECT 1;"
```

---

## Troubleshooting

### Problem: Port 5433 already in use

```bash
# Find process using port 5433
lsof -i :5433

# Kill the process (Linux/macOS)
kill -9 <PID>

# Or change port in .env
DB_PORT=5434
```

### Problem: "db service failed to start"

Check logs:
```bash
docker-compose logs db
```

Verify `.env` has `POSTGRES_PASSWORD` set (not empty).

### Problem: Scanner can't connect to database

1. Verify `DB_URL` format in `.env`:
   ```
   postgresql://trader:PASSWORD@db:5432/marketdb
   ```

2. Wait for health check to pass:
   ```bash
   docker-compose logs db | grep "accepting connections"
   ```

3. Rebuild services:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

### Problem: Permission denied errors (Linux)

Add user to docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: Streamlit dashboard shows blank or errors

```bash
# Restart dashboard
docker-compose restart dashboard

# Check logs
docker-compose logs dashboard
```

---

## Development Workflow

### 1. Make code changes
Edit files locally (e.g., `main.py`, `dashboard.py`).

### 2. Rebuild if dependencies changed
```bash
docker-compose up --build
```

### 3. Restart service if only code changed
```bash
docker-compose restart scanner
docker-compose restart dashboard
```

### 4. View changes in logs
```bash
docker-compose logs -f
```

---

## Production Deployment Notes

For production, consider:

1. Use secrets management instead of `.env` file
2. Set explicit restart policies: `restart_policy: unless-stopped`
3. Add resource limits to services:
   ```yaml
   services:
     db:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 1G
   ```
4. Use external database instead of containerized one
5. Set up proper logging (ELK stack, Datadog, etc.)
6. Use SSL/TLS for connections

---

## Cleanup

Remove everything:
```bash
# Stop and remove containers, volumes, networks
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Clean unused Docker resources
docker system prune -a
```

---

## Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Compose CLI Reference](https://docs.docker.com/compose/reference/)
- [PostgreSQL Docker Official Image](https://hub.docker.com/_/postgres)
- [Streamlit in Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

---

**Last Updated:** 2026-06-16  
**Project:** RSI Momentum
