# Smart Match API - Swagger Documentation

## 🎯 Overview

Your API now has **comprehensive Swagger/OpenAPI documentation** that's automatically generated and interactive!

## 📍 Accessing the Documentation

### Swagger UI (Interactive)
```
http://localhost:8000/docs
```
- **Interactive testing** - Try endpoints directly from the browser
- **Example requests/responses** - Multiple examples for each endpoint
- **Schema visualization** - See all data models
- **Authorization testing** - Test with different parameters

### ReDoc (Alternative UI)
```
http://localhost:8000/redoc
```
- **Clean, modern interface** - Better for reading
- **Printable** - Great for offline reference
- **Search functionality** - Find endpoints quickly

### OpenAPI JSON Schema
```
http://localhost:8000/openapi.json
```
- **Raw OpenAPI 3.0 schema** - For code generation
- **Import into tools** - Use with Postman, Insomnia, etc.

---

## ✨ What's Been Enhanced

### 1. **Rich API Metadata**

```python
{
    "title": "Smart Match API",
    "version": "1.0.0",
    "description": "Full markdown description with emojis and sections",
    "contact": {
        "name": "API Support",
        "email": "support@example.com"
    },
    "license": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
}
```

### 2. **Organized Tag Groups**

All endpoints are organized into logical groups:

| Tag | Description | Endpoints |
|-----|-------------|-----------|
| **Health** | Health checks and status | `GET /`, `GET /health` |
| **Facet Parsing** | Core parsing functionality | `POST /parse`, `GET /parse` |
| **Batch Operations** | Bulk processing | `POST /parse/batch` |
| **Schema** | Configuration and metadata | `GET /facets/schema`, `GET /facets/categories` |

### 3. **Detailed Endpoint Documentation**

Each endpoint now includes:

✅ **Comprehensive descriptions** with use cases  
✅ **Multiple example requests** (smartphone, laptop, appliance)  
✅ **Multiple example responses** (success, error, minimal)  
✅ **HTTP status codes** (200, 500, etc.)  
✅ **Query parameter documentation**  
✅ **Request/response schemas**  

### 4. **Enhanced Request Models**

**QueryRequest** - Multiple examples:
```json
{
  "examples": {
    "smartphone": {
      "summary": "Smartphone Query",
      "value": {
        "query": "iPhone 13 with 256GB in blue",
        "include_metadata": true
      }
    },
    "laptop": {...},
    "appliance": {...}
  }
}
```

### 5. **Enhanced Response Models**

**FacetsResponse** - Multiple example scenarios:
```json
{
  "examples": {
    "smartphone": {...},
    "laptop": {...},
    "minimal": {...}
  }
}
```

### 6. **New Models Added**

- `BatchQueryRequest` - For batch operations
- `BatchResponse` - Batch processing results
- `ErrorResponse` - Standardized error format

---

## 🔍 Endpoint Details

### Health Check Endpoints

#### `GET /`
```markdown
# Root Endpoint

Returns basic API information including version and status.
Use this endpoint to verify the API is accessible.
```

**Response Example:**
```json
{
  "message": "Smart Match API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "health": "/health"
}
```

#### `GET /health`
```markdown
# Health Check Endpoint

Returns the health status of the API service.
Use this for monitoring and load balancer health checks.
```

---

### Facet Parsing Endpoints

#### `POST /parse`

**Full documentation includes:**
- Description with features
- Query examples by category
- Response format explanation
- Multiple request examples
- Status code documentation

**Example curl:**
```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "iPhone 13 with 256GB in blue",
    "include_metadata": true
  }'
```

#### `GET /parse`

**Query Parameters:**
- `q` - Natural language query (required)
- `metadata` - Include metadata (optional)

**Example:**
```
http://localhost:8000/parse?q=iPhone%2013%20with%20256GB&metadata=true
```

---

### Batch Operations

#### `POST /parse/batch`

**Features documented:**
- Parallel processing capability
- Error resilience (individual failures don't stop batch)
- Flexible size (1-100 queries)
- Metadata support per query

**Example Request:**
```json
{
  "queries": [
    "iPhone 13 with 256GB in blue",
    "Gaming laptop with RTX 3060",
    "Samsung Galaxy S21 5G"
  ],
  "include_metadata": true
}
```

**Example Response:**
```json
{
  "success": true,
  "total": 3,
  "results": [
    {
      "success": true,
      "query": "iPhone 13 with 256GB in blue",
      "facets": {...},
      "facet_count": 4
    },
    ...
  ]
}
```

---

### Schema Endpoints

#### `GET /facets/schema`

Returns the complete facets configuration from `facets_config.json`.

**Use cases documented:**
- Understanding available facets
- Building search interfaces
- Validating parsed results
- Documentation generation

#### `GET /facets/categories`

Returns facets organized by product category.

**Categories:**
- Core (universal)
- Mobile Electronics
- Computing
- Home Appliances
- Gaming
- General
- Technical

---

## 🎨 Swagger UI Features

### Interactive Testing

1. **Click "Try it out"** on any endpoint
2. **Modify the example** request body
3. **Click "Execute"** to send the request
4. **View the response** with status code, headers, and body

### Example Selector

Each endpoint with multiple examples has a dropdown:
```
[Select Example ▼]
  - Smartphone Query
  - Laptop Query
  - Home Appliance Query
```

### Schema Explorer

Click on any model to see:
- All properties
- Data types
- Required vs optional fields
- Descriptions
- Default values
- Validation constraints

---

## 📚 Documentation Best Practices Used

### 1. **Markdown in Descriptions**

```python
description = """
## 🚀 Smart Match API

### Features
* **Natural Language Processing**
* **Multi-Category Support**
* **Batch Processing**

### Use Cases
* E-commerce search
* Voice-based search
* Chatbot integration
"""
```

### 2. **HTTP Status Codes**

```python
responses={
    200: {
        "description": "Successfully parsed query",
        "model": FacetsResponse
    },
    500: {
        "description": "Internal server error",
        "model": ErrorResponse
    }
}
```

### 3. **Field-Level Documentation**

```python
query: str = Field(
    ...,
    description="Natural language query to parse",
    min_length=1,
    example="iPhone 13 with 256GB"
)
```

### 4. **Multiple Examples**

```python
class Config:
    schema_extra = {
        "examples": {
            "example1": {...},
            "example2": {...}
        }
    }
```

---

## 🔧 Customization Guide

### Update Contact Information

Edit `api.py`:
```python
app = FastAPI(
    ...
    contact={
        "name": "Your Team",
        "email": "team@yourcompany.com",
        "url": "https://yourcompany.com"
    }
)
```

### Update License

```python
license_info={
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
}
```

### Add API Servers

```python
servers=[
    {
        "url": "https://api.example.com/v1",
        "description": "Production"
    },
    {
        "url": "http://localhost:8000",
        "description": "Development"
    }
]
```

### Add Security Schemes

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(
    ...
    swagger_ui_init_oauth={
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret"
    }
)
```

---

## 🚀 Quick Start

### 1. Start the API

```bash
make run
# or
make dev  # for auto-reload
```

### 2. Open Swagger UI

```
http://localhost:8000/docs
```

### 3. Try an Endpoint

1. Go to **POST /parse**
2. Click "Try it out"
3. Select an example from dropdown
4. Click "Execute"
5. View the response!

---

## 📊 Benefits

### For Developers
✅ **Self-documenting** - No need to maintain separate docs  
✅ **Interactive testing** - Test without Postman/curl  
✅ **Type safety** - Pydantic models ensure data integrity  
✅ **Code generation** - Export OpenAPI schema for client SDKs  

### For Users
✅ **Clear examples** - Multiple scenarios for each endpoint  
✅ **Easy exploration** - Browse all endpoints and features  
✅ **Quick testing** - Try the API directly from docs  
✅ **Always up-to-date** - Auto-generated from code  

---

## 🔗 Additional Resources

### FastAPI Documentation
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/tutorial/metadata/)
- [Advanced OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/)

### OpenAPI Specification
- [OpenAPI 3.0 Spec](https://swagger.io/specification/)
- [Swagger Editor](https://editor.swagger.io/)

### Tools
- **Postman**: Import OpenAPI schema for collections
- **Insomnia**: Load OpenAPI spec for testing
- **Swagger Codegen**: Generate client SDKs
- **Stoplight**: Design and mock APIs

---

## 🎉 Summary

Your API now has **professional-grade Swagger documentation** with:

✨ Rich metadata and descriptions  
✨ Multiple examples per endpoint  
✨ Organized tag groups  
✨ Interactive testing interface  
✨ Complete schema documentation  
✨ HTTP status code definitions  
✨ Field-level descriptions  
✨ Error response models  

**Access it at:** http://localhost:8000/docs

Enjoy your enhanced API documentation! 🚀

