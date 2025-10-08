# Smart Match API

A powerful AI-powered REST API that intelligently matches product queries to structured search facets. Transform natural language into precise product filters using advanced language models.

## 🎯 Overview

Smart Match uses advanced language models (GPT-4/GPT-3.5) to understand user queries and extract relevant product attributes automatically. It supports a comprehensive range of product categories including electronics, home appliances, gaming, and more.

## ✨ Features

- **Natural Language Understanding**: Converts conversational queries into structured facets
- **Comprehensive Facet Support**: 80+ product attributes across multiple categories
- **REST API**: Easy integration with FastAPI-based endpoints
- **Batch Processing**: Parse multiple queries simultaneously
- **Schema Introspection**: Explore available facets and categories
- **Real-time Processing**: Instant query parsing with OpenAI models

## 🏗️ Architecture

```
User Query → LLM Parser → Structured Facets → API Response
```

The system consists of:
- **FastAPI REST API** (`api.py`): HTTP endpoints for query processing
- **Controller** (`controller.py`): Business logic orchestration
- **Facet Parser** (`services/facet_parser.py`): LLM-based query parsing
- **Facets Schema** (`facets_config.json`): Complete facet definitions

## 📋 Supported Facets

### Core Facets
- `brand`, `model`, `cat_id`
- `price`, `price_ranges`
- `backbox_grade` (condition)

### Mobile/Electronics
- Storage, color, screen size, memory
- Processor, network (4G/5G), connectivity
- Camera, dual_sim, battery, OS
- Touch ID, Face ID, Retina display

### Computing
- Graphics card, processor type
- Storage type (SSD/HDD), touchscreen
- Screen format, webcam, HDMI ports

### Home Appliances
- Energy class, capacity, power
- Coffee machine, washing machine, fridge types
- Dishwasher, oven, hob types

### Gaming
- Console type, compatible platforms
- PEGI ratings, game genres
- Number of controllers

### General Attributes
- Warranty, deals, special offers
- Release year, generation
- Vintage, limited edition

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Poetry (Python dependency manager)
- OpenAI API key

### Installation

1. **Install Poetry** (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or visit: https://python-poetry.org/docs/#installation

2. **Clone the repository**
```bash
git clone <repository-url>
cd QnA-Langchain-VectorDB
```

3. **Setup with Poetry** (one command!)
```bash
make setup
```

This will:
- Configure Poetry to create virtual environment in the project
- Install all dependencies
- Create `.env` file from template

4. **Configure your API key**

Edit the `.env` file:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

5. **Run the API**
```bash
make run
```

Or directly with Poetry:
```bash
poetry run python api.py
```

Or in development mode with auto-reload:
```bash
make dev
```

## 📡 API Endpoints

### Health Check
```bash
GET /
GET /health
```

### Parse Query (POST)
```bash
POST /parse
Content-Type: application/json

{
  "query": "Looking for iPhone 13 with 256GB in blue under $800",
  "include_metadata": false
}
```

**Response:**
```json
{
  "success": true,
  "facets": {
    "brand": "Apple",
    "model": "iPhone 13",
    "storage": "256GB",
    "color": "blue",
    "price_ranges": {"max": 800},
    "backbox_grade": "new"
  },
  "query": "Looking for iPhone 13 with 256GB in blue under $800"
}
```

### Parse Query (GET)
```bash
GET /parse?q=Samsung Galaxy S21 5G&metadata=true
```

### Batch Processing
```bash
POST /parse/batch
Content-Type: application/json

["iPhone 11 black 128GB", "PS5 with extra controller", "Dell laptop with RTX 3060"]
```

### Get Facets Schema
```bash
GET /facets/schema
```

### Get Facet Categories
```bash
GET /facets/categories
```

## 💡 Usage Examples

### Example 1: Mobile Device
**Query:** "Show me iPhone 11 with 128GB in black"

**Response:**
```json
{
  "facets": {
    "brand": "Apple",
    "model": "iPhone 11",
    "storage": "128GB",
    "color": "black"
  }
}
```

### Example 2: Gaming Console
**Query:** "PS5 games rated 18+ in action genre"

**Response:**
```json
{
  "facets": {
    "console_type": "PlayStation",
    "compatible_gaming_console": ["PS5"],
    "pegi": "18",
    "video_game_genre": "action"
  }
}
```

### Example 3: Laptop with Price Range
**Query:** "Looking for a gaming laptop with RTX 3060 under $1500"

**Response:**
```json
{
  "facets": {
    "cat_id": "laptops",
    "graphic_card": "NVIDIA RTX 3060",
    "price_ranges": {"max": 1500}
  }
}
```

### Example 4: Home Appliance
**Query:** "Espresso coffee machine with energy class A++"

**Response:**
```json
{
  "facets": {
    "cat_id": "home_appliances",
    "coffee_machine_type": "espresso",
    "energy_class": "A++"
  }
}
```

### Example 5: Refurbished Product
**Query:** "Refurbished MacBook Pro with M1 chip"

**Response:**
```json
{
  "facets": {
    "brand": "Apple",
    "model": "MacBook Pro",
    "processor": "M1",
    "backbox_grade": "refurbished"
  }
}
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-4"  # or gpt-3.5-turbo
API_HOST = "0.0.0.0"
API_PORT = 8000
LOG_LEVEL = "INFO"
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Parse query
curl -X POST http://localhost:8000/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "iPhone 13 blue 256GB"}'

# Get schema
curl http://localhost:8000/facets/schema
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/parse",
    json={"query": "Samsung Galaxy S21 5G with dual sim"}
)
print(response.json())
```

### Using JavaScript

```javascript
fetch('http://localhost:8000/parse', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    query: "Gaming laptop with RTX 3060 under $1500"
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🏗️ Project Structure

```
.
├── api.py                      # FastAPI REST API endpoints
├── controller.py               # Business logic controller
├── config.py                   # Configuration settings
├── facets_config.json          # Complete facets schema
├── services/
│   ├── __init__.py
│   └── facet_parser.py         # LLM-based query parser
├── pyproject.toml              # Poetry dependencies and config
├── poetry.lock                 # Poetry lock file
├── Makefile                    # Development commands
├── start.sh                    # Startup script
├── README.md                   # This file
└── .env                        # Environment variables (create this)
```

## 🔒 Security

- Never commit your `.env` file or expose your OpenAI API key
- Use environment variables for sensitive configuration
- Consider rate limiting in production
- Implement authentication for production use

## ⚡ Performance

- **GPT-4**: More accurate but slower (~2-4s per query)
- **GPT-3.5-turbo**: Faster and cheaper (~1-2s per query), slightly less accurate
- Use batch endpoint for multiple queries
- Consider caching frequent queries

## 🐛 Troubleshooting

### OpenAI API Key Error
```
Error: OpenAI API key not set
```
**Solution**: Set the `OPENAI_API_KEY` environment variable

### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Reinstall dependencies: `poetry install`

### Port Already in Use
```
Error: [Errno 48] Address already in use
```
**Solution**: Change port in config.py or kill the process using the port

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Your License Here]

## 📧 Contact

For questions or support, please [create an issue](your-repo-url/issues).

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Uses [LangChain](https://langchain.com/)

---

**Note**: This system is designed for product search and filtering. Accuracy depends on the quality of user queries and the LLM model used. For production use, consider implementing query validation, result verification, and fallback mechanisms.
