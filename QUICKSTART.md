# Quick Start Guide

## Prerequisites

- Python 3.9+
- Poetry (Python dependency manager)
- OpenAI API key

## Install Poetry

If you don't have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or visit: https://python-poetry.org/docs/#installation

## Step 1: Setup with Poetry

```bash
# One command to set everything up!
make setup
```

This will:
- Configure Poetry for the project
- Install all dependencies
- Create .env file from template

**Or manually:**

```bash
# Install dependencies
poetry install

# Copy environment template
cp env.example .env
```

## Step 2: Configure Environment

Edit the `.env` file and add your OpenAI API key:

```bash
# Open .env in your editor
nano .env

# Or use sed to replace
sed -i '' 's/your-openai-api-key-here/sk-YOUR_ACTUAL_KEY/' .env
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-proj-...your-key-here...
OPENAI_MODEL=gpt-4
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## Step 3: Start the API

**Option 1: Using Make (recommended)**
```bash
make run
```

**Option 2: Using start script**
```bash
./start.sh
```

**Option 3: Using Poetry directly**
```bash
poetry run python api.py
```

**Option 4: Development mode (with auto-reload)**
```bash
make dev
```

## Step 4: Test the API

### Open API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test with cURL
```bash
curl -X POST http://localhost:8000/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "iPhone 13 blue 256GB under $800"}'
```

### Run Test Script
```bash
make test
# or
poetry run python test_api.py
```

## Example Usage

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/parse",
    json={"query": "Samsung Galaxy S21 5G with dual sim"}
)

print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:8000/parse', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: "Gaming laptop with RTX 3060"})
})
.then(res => res.json())
.then(console.log);
```

### cURL (GET method)
```bash
curl "http://localhost:8000/parse?q=iPhone+11+black+128GB"
```

## Common Queries

1. **Mobile Device**
   ```
   "iPhone 13 with 256GB in blue color"
   ```

2. **Laptop**
   ```
   "Gaming laptop with RTX 3060 and 16GB RAM under $1500"
   ```

3. **Refurbished Product**
   ```
   "Refurbished MacBook Pro with M1 chip"
   ```

4. **Home Appliance**
   ```
   "Espresso coffee machine with energy class A++"
   ```

5. **Gaming**
   ```
   "PS5 games rated 18+ in action genre"
   ```

## Useful Commands

### Development
```bash
make setup      # Initial setup
make run        # Run API
make dev        # Run with auto-reload
make test       # Run tests
make docs       # Open docs in browser
```

### Poetry Commands
```bash
poetry shell    # Activate virtual environment
poetry install  # Install dependencies
poetry update   # Update dependencies
poetry show     # Show installed packages
poetry add <pkg># Add new package
```

### Maintenance
```bash
make clean      # Clean cache files
make clean-all  # Remove venv and lock file
make show       # Show installed packages
```

## Troubleshooting

### Problem: "Poetry not found"
**Solution:** Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Problem: "OpenAI API key not set"
**Solution:** Check your .env file and ensure OPENAI_API_KEY is set

### Problem: "Port already in use"
**Solution:** Change API_PORT in .env or kill the existing process:
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Problem: Import errors
**Solution:** Reinstall dependencies:
```bash
poetry install
```

### Problem: Dependencies not found
**Solution:** Make sure you're using Poetry:
```bash
poetry run python api.py
# or activate the shell first
poetry shell
python api.py
```

## Next Steps

- Read the full [README.md](README.md)
- Explore API documentation at `/docs`
- Check out example queries in [EXAMPLES.md](EXAMPLES.md)
- Review the facets schema at `/facets/schema`
- Integrate the API into your application

## Quick Reference

| Action | Command |
|--------|---------|
| Setup everything | `make setup` |
| Install deps | `poetry install` |
| Run API | `make run` |
| Dev mode | `make dev` |
| Run tests | `make test` |
| Open docs | `make docs` |
| Shell | `poetry shell` |
| Clean | `make clean` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your OpenAI API key (required) |
| `OPENAI_MODEL` | gpt-4 | Model to use (gpt-4 or gpt-3.5-turbo) |
| `API_HOST` | 0.0.0.0 | API server host |
| `API_PORT` | 8000 | API server port |
| `LOG_LEVEL` | INFO | Logging level |

---

**You're ready to go! 🚀**

Start with: `make setup` → Edit `.env` → `make run`
