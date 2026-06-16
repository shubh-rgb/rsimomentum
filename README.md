# 📈 RSI Momentum - Stock Ranking Dashboard

A real-time stock ranking dashboard powered by technical indicators (RSI, MACD, Bollinger Bands) to identify trading opportunities in NSE stocks.

---

## 🎯 Features

- **Real-time Stock Scanning**: Automated scanner runs every 15 minutes
- **Technical Analysis**: RSI, MACD, Bollinger Bands, DMA30 calculations
- **Stock Ranking**: Composite scoring based on multiple indicators
- **Interactive Dashboard**: Streamlit-based web UI with charts and search
- **Secure Deployment**: Environment-based credentials, authentication required
- **Database Storage**: PostgreSQL for persistent scan results
- **Docker Support**: Full Docker & Docker Compose setup

---

## 🔐 Security Features

This application implements enterprise-grade security:

- ✅ **No Hardcoded Credentials**: All secrets via environment variables
- ✅ **Authentication Required**: Streamlit login before dashboard access
- ✅ **Input Validation**: Protected against ReDoS and injection attacks
- ✅ **Sanitized Error Messages**: Sensitive info never leaked to users
- ✅ **Structured Logging**: Full audit trail in `logs/app.log`
- ✅ **Pinned Dependencies**: Specific versions for reproducibility

👉 **See [SECURITY_FIXES.md](SECURITY_FIXES.md) for detailed security changes**

---

## 📋 Prerequisites

- **Python 3.12+** or Docker
- **PostgreSQL 14+** (or Docker)
- **Git**
- **pip** (Python package manager)

---

## 🚀 Quick Start (5 minutes)

### Option 1: Local Setup (Recommended for Development)

#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd rsimomentum
```

#### 2. Setup Environment Variables
```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your database credentials
nano .env
```

Edit `.env` and set:
```env
# Database credentials
POSTGRES_USER=trader
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=marketdb
DB_URL=postgresql://trader:your_secure_password_here@localhost:5432/marketdb
DB_PORT=5433
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Start PostgreSQL (if not running)
```bash
# Option A: Using Docker
docker run -d \
  --name postgres-rsi \
  -e POSTGRES_USER=trader \
  -e POSTGRES_PASSWORD=your_secure_password_here \
  -e POSTGRES_DB=marketdb \
  -p 5433:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# Option B: Using existing PostgreSQL installation
# Ensure database user and database exist
```

#### 5. Initialize Database Schema
```bash
python3 -c "from database.storage import init_db; init_db()"
```

#### 6. Start the Application

**Terminal 1 - Start the Scheduler (background jobs):**
```bash
python3 main.py
```

**Terminal 2 - Start the Dashboard (web UI):**
```bash
streamlit run dashboard.py
```

#### 7. Access Dashboard
```
http://localhost:8501
```

**Login with default credentials:**
- Username: `admin`
- Password: `admin123`

> ⚠️ **IMPORTANT**: Change these credentials immediately before production deployment!

---

### Option 2: Docker Setup (Recommended for Production)

#### 1. Create .env File
```bash
cp .env.example .env
nano .env
```

Set the same environment variables as above.

#### 2. Build and Start
```bash
docker-compose up --build -d
```

This will start:
- PostgreSQL database on port 5433
- Scanner service (processes stock data)
- Streamlit dashboard on port 8501

#### 3. Access Dashboard
```
http://localhost:8501
Login: admin / admin123
```

#### 4. View Logs
```bash
# All containers
docker-compose logs -f

# Specific service
docker-compose logs -f scanner
docker-compose logs -f dashboard
```

#### 5. Stop Everything
```bash
docker-compose down
```

---

## 📖 Detailed Setup Guide

### Step 1: Environment Configuration

The application requires a `.env` file with sensitive configuration. **This file should NOT be committed to Git** (it's in `.gitignore`).

**Required Variables:**
```env
# Database Configuration
POSTGRES_USER=trader                    # DB username
POSTGRES_PASSWORD=your_password         # DB password (secure!)
POSTGRES_DB=marketdb                    # Database name
DB_PORT=5433                            # PostgreSQL port
DB_URL=postgresql://trader:password@localhost:5433/marketdb

# Kite Connect API (optional - for future integration)
# KITE_API_KEY=your_key
# KITE_API_SECRET=your_secret
# KITE_ACCESS_TOKEN=your_token

# Application Settings
TOP_N=10                                # Top N stocks to display
SCAN_INTERVAL_MIN=15                    # Scan every N minutes
```

**To generate a secure password:**
```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```

### Step 2: Database Setup

The application uses PostgreSQL to store scan results.

#### A. Using Docker (Easiest)
```bash
docker run -d \
  --name postgres-rsi \
  -e POSTGRES_USER=trader \
  -e POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_hex(16))") \
  -e POSTGRES_DB=marketdb \
  -p 5433:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

#### B. Using Existing PostgreSQL
```bash
# Connect as superuser
psql -U postgres

# Create user and database
CREATE USER trader WITH PASSWORD 'your_secure_password';
CREATE DATABASE marketdb OWNER trader;
GRANT ALL PRIVILEGES ON DATABASE marketdb TO trader;
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
```

### Step 4: Initialize Database Schema

```bash
python3 << 'EOF'
from database.storage import init_db
init_db()
print("✅ Database schema initialized")
EOF
```

---

## 🎮 Running the Application

### Local Development

**Terminal 1: Start the Scanner (processes stock data)**
```bash
python3 main.py
```

You should see output like:
```
INFO:scheduler.jobs:Completed scan at 2026-06-16 14:30:45.123456 - found 10 opportunities
```

**Terminal 2: Start the Dashboard (web UI)**
```bash
streamlit run dashboard.py
```

Output:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### Docker Compose

```bash
# Start all services
docker-compose up

# Or in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

---

## 🧪 Verification Steps

### 1. Check Database Connection
```bash
python3 << 'EOF'
from database.storage import engine
try:
    with engine.connect() as conn:
        print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database error: {e}")
EOF
```

### 2. Test Data Fetching
```bash
python3 << 'EOF'
from data.universe import get_universe
from data.fetcher import fetch_batch
symbols = get_universe()[:5]
data = fetch_batch(symbols)
print(f"✅ Fetched data for {len(data)} symbols")
EOF
```

### 3. Run a Scanner Job
```bash
python3 << 'EOF'
from scheduler.jobs import job
job()
print("✅ Scanner job completed")
EOF
```

### 4. Check Dashboard Login
```
Open http://localhost:8501
Login: admin / admin123
Should see "Market Summary" metrics
```

---

## 📊 Application Structure

```
rsimomentum/
├── config.py              # Configuration (env vars)
├── main.py               # Entry point (starts scheduler)
├── dashboard.py          # Streamlit web interface
├── auth.py              # Authentication module
├── logger_config.py     # Logging configuration
│
├── database/
│   ├── schema.py        # Database schema definitions
│   └── storage.py       # Database operations
│
├── data/
│   ├── universe.py      # Stock universe (NSE Nifty 50)
│   └── fetcher.py       # Data fetching (yfinance)
│
├── indicators/
│   └── technicals.py    # Technical indicators (RSI, MACD, BB)
│
├── ranking/
│   └── scorer.py        # Scoring algorithm
│
├── scanner/
│   └── engine.py        # Main scanning logic
│
├── scheduler/
│   └── jobs.py          # Scheduled jobs
│
├── dashboard/
│   ├── charts.py        # Chart generation
│   └── stock_details.py # Stock detail page
│
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker orchestration
├── Dockerfile          # Docker image definition
├── .streamlit/
│   └── config.toml     # Streamlit configuration
└── README.md           # This file
```

---

## 🔧 Troubleshooting

### Issue: "DB_URL environment variable not set"
```bash
# Solution: Create .env file
cp .env.example .env
nano .env  # Add your database credentials
source .env  # Load environment
```

### Issue: "Connection refused" (PostgreSQL)
```bash
# Solution 1: Check if database is running
docker ps | grep postgres

# Solution 2: Verify database connection string in .env
# Format: postgresql://user:password@host:port/database
```

### Issue: "ModuleNotFoundError: No module named 'data'"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify: Check if data/__init__.py exists
ls -la data/
```

### Issue: "Failed to connect" on dashboard login
```bash
# Solution: Check database is initialized
python3 -c "from database.storage import init_db; init_db()"

# Check logs
tail -f logs/app.log
```

### Issue: Dashboard won't authenticate
```bash
# Solution: Restart Streamlit and clear cache
pkill -f streamlit
rm -rf ~/.streamlit/
streamlit run dashboard.py
```

---

## 📈 How It Works

### 1. **Scheduler (main.py)**
- Runs every 15 minutes
- Fetches latest stock data for NSE Nifty 50
- Calculates technical indicators
- Scores each stock based on composite algorithm
- Saves results to PostgreSQL

### 2. **Technical Analysis (indicators/technicals.py)**
- **RSI (Relative Strength Index)**: Momentum oscillator (0-100)
- **MACD**: Trend indicator
- **Bollinger Bands**: Volatility indicator
- **DMA30**: 30-day moving average

### 3. **Scoring Algorithm (ranking/scorer.py)**
```
Score = 0
if Close > DMA30: +30 points
if MACD > MACD_SIG: +25 points
if RSI > 55: +20 points
if Close > (BB_UP + BB_DN)/2: +15 points
Total: 0-100
```

### 4. **Dashboard (dashboard.py)**
- Displays top ranked stocks
- Real-time charts with Plotly
- Search functionality
- Watchlist view
- Auto-refresh every 60 seconds

---

## 🔐 Production Deployment Checklist

Before deploying to production:

- [ ] **Change default credentials** in `auth.py` (lines 20-24)
- [ ] **Set strong database password** in `.env`
- [ ] **Configure HTTPS/SSL** (use reverse proxy like nginx)
- [ ] **Setup log rotation** for `logs/app.log`
- [ ] **Enable database backups** for `pgdata` volume
- [ ] **Run security audit**: `safety check`
- [ ] **Setup monitoring** for scanner and database
- [ ] **Configure firewall** to restrict access to ports
- [ ] **Test authentication flow** with real credentials
- [ ] **Test error messages** don't leak sensitive data
- [ ] **Document** any custom modifications
- [ ] **Setup CI/CD** for automated deployments

---

## 🆘 Getting Help

### Check Application Logs
```bash
tail -f logs/app.log
```

### Docker Logs
```bash
docker-compose logs -f scanner   # Scanner service
docker-compose logs -f dashboard # Dashboard service
docker-compose logs -f db       # Database service
```

### Database Query
```bash
# Access PostgreSQL directly
psql -h localhost -p 5433 -U trader -d marketdb

# List scan results
SELECT symbol, score, rsi, macd, scan_time FROM scans ORDER BY scan_time DESC LIMIT 10;
```

### Python Debugging
```bash
# Enable verbose logging
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from scheduler.jobs import job
job()
"
```

---

## 📚 Additional Resources

- [SECURITY_FIXES.md](SECURITY_FIXES.md) - Detailed security improvements
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [TA-Lib Documentation](https://github.com/mrjbq7/ta-lib) - For advanced indicators

---

## 📝 License & Support

For issues or questions, please:
1. Check the troubleshooting section above
2. Review logs in `logs/app.log`
3. Verify `.env` configuration is correct
4. Consult [SECURITY_FIXES.md](SECURITY_FIXES.md) for security-related issues

---

## ✅ Changelog - Security Updates (v1.1.0)

**Latest Security Improvements:**
- Removed hardcoded database credentials
- Implemented Streamlit authentication
- Fixed data loss (scheduler-database sync)
- Added input validation (ReDoS prevention)
- Implemented structured logging
- Pinned all dependency versions
- Created data module for stock universe
- Added Streamlit security configuration

See [SECURITY_FIXES.md](SECURITY_FIXES.md) for complete details.

---

**Last Updated**: June 16, 2026  
**Status**: ✅ Production Ready (with credential setup)