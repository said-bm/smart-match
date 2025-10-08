"""
Smart Match API - FastAPI REST API for Intelligent Product Matching
Converts natural language queries into structured product search facets
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import logging
from controller import Controller
import config as cfg

# Configure logging
logging.basicConfig(level=cfg.LOG_LEVEL)
logger = logging.getLogger(__name__)

# API Metadata for Swagger
DESCRIPTION = """
## 🚀 Smart Match API

Intelligent product matching that transforms natural language queries into structured, searchable facets using AI-powered parsing.

### Features

* **Natural Language Processing**: Convert human-readable queries into structured data
* **Direct Facet Configuration**: Submit facets directly without AI parsing
* **Multi-Category Support**: Handle various product categories (electronics, appliances, gaming, etc.)
* **Batch Processing**: Parse multiple queries simultaneously
* **Flexible Input**: Support both GET and POST requests
* **Schema Validation**: Optional validation of facet structures
* **Rich Metadata**: Optional detailed metadata in responses
* **Schema Introspection**: Query available facets and categories

### Use Cases

* E-commerce search enhancement
* Voice-based product search
* Chatbot integration
* Search analytics
* Product recommendation systems

### Example Natural Language Queries

* "Show me iPhone 13 with 256GB in blue under $800"
* "Gaming laptop with RTX 3060 and 16GB RAM"
* "Samsung Galaxy S21 5G with dual sim"
* "Espresso machine with energy class A++"
* "PS5 games rated 18+ in action genre"

### Direct Facet Configuration

You can also submit facets directly via `POST /facets/configure`:

```json
{
  "facets": {
    "brand": "Apple",
    "model": "iPhone 13",
    "storage": "256GB",
    "color": "blue"
  },
  "validate_schema": true
}
```

---
**Note**: Natural language parsing requires OpenAI API key. Direct configuration works without AI.
"""

TAGS_METADATA = [
    {
        "name": "Health",
        "description": "Health check and service status endpoints",
    },
    {
        "name": "Facet Parsing",
        "description": "Core endpoints for parsing natural language queries into structured facets",
    },
    {
        "name": "Schema",
        "description": "Endpoints for retrieving facet schemas and available categories",
    },
    {
        "name": "Batch Operations",
        "description": "Endpoints for processing multiple queries at once",
    },
]

# Initialize FastAPI app with enhanced metadata
app = FastAPI(
    title=cfg.API_TITLE,
    description=DESCRIPTION,
    version=cfg.API_VERSION,
    openapi_tags=TAGS_METADATA,
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controller
controller = Controller()


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for query parsing"""
    query: str = Field(
        ..., 
        description="Natural language query to parse into product facets",
        min_length=1
    )
    include_metadata: bool = Field(
        False, 
        description="Include additional metadata such as facet count and detected categories in the response"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "query": "iPhone 13 with 256GB storage in blue under $800",
                "include_metadata": True
            }
        }


class FacetsResponse(BaseModel):
    """Response model for parsed facets"""
    success: bool = Field(..., description="Whether the parsing was successful")
    facets: Dict[str, Any] = Field(..., description="Extracted product facets as key-value pairs")
    query: Optional[str] = Field(None, description="Original query that was parsed")
    facet_count: Optional[int] = Field(None, description="Total number of facets extracted (only if metadata enabled)")
    categories_detected: Optional[List[str]] = Field(None, description="Detected product categories (only if metadata enabled)")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "facets": {
                    "brand": "Apple",
                    "model": "iPhone 13",
                    "storage": "256GB",
                    "color": "blue",
                    "price_ranges": {"max": 800},
                    "backbox_grade": "new"
                },
                "query": "iPhone 13 with 256GB in blue under $800",
                "facet_count": 6,
                "categories_detected": ["mobile_electronics"]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message describing what went wrong")
    details: Optional[str] = Field(None, description="Additional error details or stack trace")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Failed to parse query",
                "details": "OpenAI API key not configured or invalid"
            }
        }


class BatchQueryRequest(BaseModel):
    """Request model for batch query parsing"""
    queries: List[str] = Field(
        ..., 
        description="List of natural language queries to parse",
        min_items=1,
        max_items=100
    )
    include_metadata: bool = Field(
        False,
        description="Include additional metadata for each parsed query"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "queries": [
                    "iPhone 13 with 256GB in blue",
                    "Gaming laptop with RTX 3060",
                    "Samsung Galaxy S21 5G"
                ],
                "include_metadata": True
            }
        }


class BatchResponse(BaseModel):
    """Response model for batch parsing"""
    success: bool = Field(..., description="Whether the batch processing was successful")
    total: int = Field(..., description="Total number of queries processed")
    results: List[Dict[str, Any]] = Field(..., description="List of parsed results")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "total": 3,
                "results": [
                    {
                        "success": True,
                        "query": "iPhone 13 with 256GB in blue",
                        "facets": {
                            "brand": "Apple",
                            "model": "iPhone 13",
                            "storage": "256GB",
                            "color": "blue"
                        },
                        "facet_count": 4
                    },
                    {
                        "success": True,
                        "query": "Gaming laptop with RTX 3060",
                        "facets": {
                            "graphic_card": "RTX 3060",
                            "cat_id": "laptops"
                        },
                        "facet_count": 2
                    }
                ]
            }
        }


class DirectFacetsRequest(BaseModel):
    """Request model for direct facet configuration"""
    facets: Dict[str, Any] = Field(
        ...,
        description="Direct facet configuration as key-value pairs"
    )
    validate_schema: bool = Field(
        True,
        description="Validate facets against the schema"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "facets": {
                    "brand": "Apple",
                    "model": "iPhone 13",
                    "storage": "256GB",
                    "color": "blue",
                    "price_ranges": {"max": 800},
                    "backbox_grade": "new",
                    "network": "5G"
                },
                "validate_schema": True
            }
        }


class DirectFacetsResponse(BaseModel):
    """Response model for direct facet configuration"""
    success: bool = Field(..., description="Whether the facet configuration was successful")
    facets: Dict[str, Any] = Field(..., description="Processed facet configuration")
    validation_errors: Optional[List[str]] = Field(None, description="Validation errors if any")
    facet_count: int = Field(..., description="Number of facets provided")
    valid_facets: Optional[List[str]] = Field(None, description="List of valid facet keys")
    invalid_facets: Optional[List[str]] = Field(None, description="List of invalid facet keys")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "facets": {
                    "brand": "Apple",
                    "model": "iPhone 13",
                    "storage": "256GB",
                    "color": "blue",
                    "price_ranges": {"max": 800},
                    "backbox_grade": "new"
                },
                "validation_errors": None,
                "facet_count": 6,
                "valid_facets": ["brand", "model", "storage", "color", "price_ranges", "backbox_grade"],
                "invalid_facets": []
            }
        }


# API Endpoints

@app.get(
    "/", 
    tags=["Health"],
    summary="API Root",
    response_description="API information and status"
)
async def root():
    """
    # Root Endpoint
    
    Returns basic API information including version and status.
    Use this endpoint to verify the API is accessible.
    """
    return {
        "message": "Smart Match API",
        "version": cfg.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health", 
    tags=["Health"],
    summary="Health Check",
    response_description="Service health status",
    status_code=status.HTTP_200_OK
)
async def health_check():
    """
    # Health Check Endpoint
    
    Returns the health status of the API service.
    Use this for monitoring and load balancer health checks.
    
    **Returns:**
    - `status`: Current health status (healthy/unhealthy)
    - `service`: Service name
    """
    return {
        "status": "healthy",
        "service": cfg.API_TITLE
    }


@app.post(
    "/parse",
    response_model=FacetsResponse,
    tags=["Facet Parsing"],
    summary="Parse Query (POST)",
    response_description="Parsed product facets",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully parsed query into facets",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "facets": {
                            "brand": "Apple",
                            "model": "iPhone 13",
                            "storage": "256GB",
                            "color": "blue"
                        },
                        "query": "iPhone 13 with 256GB in blue"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error or parsing failure",
            "model": ErrorResponse
        }
    }
)
async def parse_query(request: QueryRequest):
    """
    # Parse Natural Language Query
    
    Transform a natural language product query into structured, searchable facets using AI.
    
    ## Description
    
    This endpoint accepts a natural language query and returns structured
    product facets that can be used for filtering and searching products in your catalog.
    
    ## Features
    
    - **AI-Powered**: Uses OpenAI GPT models for intelligent parsing
    - **Multi-Domain**: Handles various product categories (electronics, appliances, gaming, etc.)
    - **Flexible**: Accepts conversational, keyword, or mixed query formats
    - **Metadata**: Optional detailed analysis and categorization
    
    ## Query Examples
    
    **Electronics:**
    - "Show me iPhone 11 with 128GB in black"
    - "Looking for a gaming laptop with RTX 3060 under $1500"
    - "Samsung Galaxy S21 5G with dual sim"
    
    **Home Appliances:**
    - "Espresso coffee machine with energy class A++"
    - "Washing machine with 8kg capacity and A+++ rating"
    
    **Gaming:**
    - "PS5 games rated 18+ in action genre"
    - "Xbox Series X with 1TB storage"
    
    ## Response Format
    
    The response includes:
    - `success`: Boolean indicating parsing success
    - `facets`: Dictionary of extracted facets (key-value pairs)
    - `query`: Original query string
    - `facet_count`: Number of facets (if metadata enabled)
    - `categories_detected`: Product categories (if metadata enabled)
    """
    try:
        logger.info(f"Parsing query: {request.query}")
        
        if request.include_metadata:
            result = controller.parse_query_with_metadata(request.query)
            return FacetsResponse(
                success=True,
                **result
            )
        else:
            facets = controller.parse_query(request.query)
            return FacetsResponse(
                success=True,
                facets=facets,
                query=request.query
            )
    
    except Exception as e:
        logger.error(f"Error parsing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse query: {str(e)}"
        )


@app.get(
    "/parse",
    response_model=FacetsResponse,
    tags=["Facet Parsing"],
    summary="Parse Query (GET)",
    response_description="Parsed product facets",
    status_code=status.HTTP_200_OK
)
async def parse_query_get(
    q: str = Query(
        ..., 
        description="Natural language query to parse", 
        min_length=1
    ),
    metadata: bool = Query(
        False, 
        description="Include additional metadata in response"
    )
):
    """
    # Parse Query via GET Request
    
    GET version of the /parse endpoint for simpler integrations and browser testing.
    
    ## Use Cases
    
    - Quick testing from browser
    - Simple webhook integrations
    - URL-based query sharing
    - GET-only HTTP clients
    
    ## Query Parameters
    
    - `q`: The natural language query to parse (required)
    - `metadata`: Include facet count and category detection (optional, default: false)
    
    ## Example Usage
    
    ```
    GET /parse?q=iPhone%2013%20with%20256GB%20in%20blue&metadata=true
    ```
    """
    request = QueryRequest(query=q, include_metadata=metadata)
    return await parse_query(request)


@app.post(
    "/facets/configure",
    response_model=DirectFacetsResponse,
    tags=["Facet Parsing"],
    summary="Configure Facets Directly",
    response_description="Validated facet configuration",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully configured and validated facets",
            "model": DirectFacetsResponse
        },
        400: {
            "description": "Invalid facet configuration",
            "model": ErrorResponse
        }
    }
)
async def configure_facets_directly(request: DirectFacetsRequest):
    """
    # Configure Facets Directly
    
    Submit facets directly without natural language parsing. Useful for programmatic access.
    
    ## Description
    
    This endpoint allows you to submit product facets directly as a structured JSON object,
    bypassing the AI-powered natural language parsing. This is useful when:
    
    - You already have structured facet data
    - You want to avoid AI processing costs
    - You need deterministic, instant responses
    - You're integrating from another system with known facet structures
    
    ## Features
    
    - **No AI Processing**: Direct facet submission without LLM calls
    - **Schema Validation**: Optional validation against the facets schema
    - **Fast**: Instant response without AI latency
    - **Deterministic**: Consistent results every time
    - **Validation Feedback**: Detailed information about valid/invalid facets
    
    ## Use Cases
    
    - **System Integration**: Connecting external systems with known data structures
    - **Testing**: Testing search functionality with specific facet combinations
    - **Migration**: Importing data from legacy systems
    - **API Chaining**: Using output from other services as input
    - **Cost Optimization**: Avoiding AI costs when facets are already known
    
    ## Facet Structure
    
    Submit any combination of valid facets:
    
    **Core Facets:**
    - `brand`, `model`, `cat_id`, `price`, `price_ranges`, `backbox_grade`
    
    **Electronics:**
    - `storage`, `color`, `screen_size`, `memory`, `processor`, `network`, `camera`
    
    **Computing:**
    - `graphic_card`, `processor_type`, `storage_type`, `touchscreen`, `webcam`
    
    **Appliances:**
    - `energy_class`, `capacity`, `power`, `coffee_machine_type`
    
    **Gaming:**
    - `console_type`, `pegi`, `video_game_genre`
    
    ## Validation
    
    When `validate_schema: true`:
    - Checks if facet keys exist in the schema
    - Returns `valid_facets` and `invalid_facets` lists
    - Provides validation errors if any
    
    When `validate_schema: false`:
    - Accepts any facet structure
    - No validation performed
    - Faster processing
    
    ## Example Request
    
    ```json
    {
      "facets": {
        "brand": "Apple",
        "model": "iPhone 13",
        "storage": "256GB",
        "color": "blue",
        "network": "5G",
        "price_ranges": {"max": 800}
      },
      "validate_schema": true
    }
    ```
    
    ## Response
    
    Returns:
    - `success`: Configuration success status
    - `facets`: The configured facets (cleaned if validated)
    - `facet_count`: Number of facets
    - `valid_facets`: List of valid facet keys (if validated)
    - `invalid_facets`: List of invalid facet keys (if validated)
    - `validation_errors`: Any validation error messages
    """
    try:
        logger.info(f"Configuring facets directly: {len(request.facets)} facets")
        
        facets = request.facets
        facet_count = len(facets)
        valid_facets = []
        invalid_facets = []
        validation_errors = []
        
        if request.validate_schema:
            # Load facets schema for validation
            try:
                import json
                with open(cfg.FACETS_CONFIG_PATH, 'r') as f:
                    schema = json.load(f)
                
                # Get all valid facet keys from schema
                all_valid_keys = set()
                if 'facets' in schema:
                    for facet_config in schema['facets']:
                        if 'key' in facet_config:
                            all_valid_keys.add(facet_config['key'])
                
                # Validate each facet key
                for facet_key in facets.keys():
                    if facet_key in all_valid_keys:
                        valid_facets.append(facet_key)
                    else:
                        invalid_facets.append(facet_key)
                        validation_errors.append(f"Unknown facet key: '{facet_key}'")
                
                logger.info(f"Validation: {len(valid_facets)} valid, {len(invalid_facets)} invalid")
                
            except FileNotFoundError:
                validation_errors.append("Facets schema file not found")
                logger.warning("Could not load facets schema for validation")
            except Exception as e:
                validation_errors.append(f"Schema validation error: {str(e)}")
                logger.error(f"Error during schema validation: {str(e)}")
        
        # If there are invalid facets and validation is enabled, return error
        if request.validate_schema and invalid_facets:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid facet configuration",
                    "invalid_facets": invalid_facets,
                    "validation_errors": validation_errors
                }
            )
        
        return DirectFacetsResponse(
            success=True,
            facets=facets,
            validation_errors=validation_errors if validation_errors else None,
            facet_count=facet_count,
            valid_facets=valid_facets if request.validate_schema else None,
            invalid_facets=invalid_facets if request.validate_schema else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error configuring facets: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to configure facets: {str(e)}"
        )


@app.get(
    "/facets/schema",
    tags=["Schema"],
    summary="Get Facets Schema",
    response_description="Complete facets configuration schema",
    status_code=status.HTTP_200_OK
)
async def get_facets_schema():
    """
    # Get Complete Facets Schema
    
    Returns the full configuration schema of all available product facets.
    
    ## Description
    
    This endpoint provides the complete facets configuration including:
    - All available facet types
    - Possible values for each facet
    - Facet descriptions and constraints
    - Category-specific facets
    
    ## Use Cases
    
    - Understanding available facets
    - Building search interfaces
    - Validating parsed results
    - Documentation generation
    - Testing and development
    """
    try:
        import json
        with open(cfg.FACETS_CONFIG_PATH, 'r') as f:
            schema = json.load(f)
        return {
            "success": True,
            "schema": schema
        }
    except Exception as e:
        logger.error(f"Error loading facets schema: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load facets schema: {str(e)}"
        )


@app.get(
    "/facets/categories",
    tags=["Schema"],
    summary="Get Facet Categories",
    response_description="Available facet categories and their facets",
    status_code=status.HTTP_200_OK
)
async def get_facet_categories():
    """
    # Get Facet Categories
    
    Returns all available product categories and their associated facets.
    
    ## Description
    
    This endpoint provides a hierarchical view of facets organized by category,
    making it easier to understand which facets apply to which product types.
    
    ## Categories
    
    - **Core**: Universal facets (brand, model, price, etc.)
    - **Mobile Electronics**: Smartphones, tablets (storage, color, network, etc.)
    - **Computing**: Laptops, desktops (processor, graphics card, RAM, etc.)
    - **Home Appliances**: Kitchen, laundry (energy class, capacity, power, etc.)
    - **Gaming**: Consoles, games (platform, rating, genre, etc.)
    - **General**: Cross-category attributes (warranty, deals, release date, etc.)
    - **Technical**: System facets (merchant ID, state, etc.)
    """
    return {
        "success": True,
        "categories": {
            "core": ["brand", "model", "cat_id", "price", "price_ranges", "backbox_grade"],
            "mobile_electronics": [
                "storage", "color", "screen_size", "memory", "processor", "network",
                "connectivity", "camera", "dual_sim", "battery_capacity", "os"
            ],
            "computing": [
                "graphic_card", "processor_type", "storage_type", "touchscreen",
                "webcam", "screen_format", "screen_type"
            ],
            "home_appliances": [
                "energy_class", "capacity", "power", "coffee_machine_type",
                "washing_machine_type", "fridge_type"
            ],
            "gaming": [
                "console_type", "compatible_gaming_console", "pegi",
                "video_game_genre", "controllers_number"
            ],
            "general": [
                "warranty", "deals_type", "special_offer_type", "year_date_release",
                "generation", "vintage", "limited_edition"
            ],
            "technical": [
                "merchant_id", "deduplication_id", "is_cheapest_listing",
                "publication_state", "backbox"
            ]
        }
    }


@app.post(
    "/parse/batch",
    response_model=BatchResponse,
    tags=["Batch Operations"],
    summary="Batch Parse Queries",
    response_description="Batch parsing results",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully parsed all queries",
            "model": BatchResponse
        },
        500: {
            "description": "Batch processing error",
            "model": ErrorResponse
        }
    }
)
async def parse_queries_batch(request: BatchQueryRequest):
    """
    # Batch Query Parsing
    
    Parse multiple natural language queries simultaneously for efficient processing.
    
    ## Description
    
    This endpoint allows you to submit multiple queries at once, reducing network overhead
    and improving throughput for bulk operations.
    
    ## Features
    
    - **Parallel Processing**: Process multiple queries efficiently
    - **Error Resilience**: Individual query failures don't stop the batch
    - **Flexible Size**: Handle 1-100 queries per request
    - **Metadata Support**: Optional metadata for each query
    
    ## Use Cases
    
    - Bulk data migration
    - Search analytics processing
    - Training data generation
    - A/B testing query variations
    - Historical data enrichment
    
    ## Limits
    
    - Minimum: 1 query
    - Maximum: 100 queries per request
    - For larger batches, split into multiple requests
    
    ## Response Format
    
    Each result in the response includes:
    - `success`: Whether that specific query parsed successfully
    - `query`: The original query
    - `facets`: Extracted facets (if successful)
    - `error`: Error message (if failed)
    """
    try:
        results = []
        for query in request.queries:
            try:
                if request.include_metadata:
                    result = controller.parse_query_with_metadata(query)
                    results.append({
                        "success": True,
                        **result
                    })
                else:
                    facets = controller.parse_query(query)
                    results.append({
                        "success": True,
                        "query": query,
                        "facets": facets
                    })
            except Exception as e:
                logger.error(f"Error parsing query '{query}': {str(e)}")
                results.append({
                    "success": False,
                    "query": query,
                    "error": str(e)
                })
        
        return BatchResponse(
            success=True,
            total=len(request.queries),
            results=results
        )
    
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process batch: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=cfg.API_HOST,
        port=cfg.API_PORT,
        log_level=cfg.LOG_LEVEL.lower()
    )

