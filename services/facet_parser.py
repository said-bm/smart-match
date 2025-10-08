import json
import os
from typing import Dict, Any
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class FacetResponse(BaseModel):
    """Structured response for product facets extracted from user query"""
    
    # Core facets
    brand: Optional[str] = Field(None, description="Product brand")
    model: Optional[str] = Field(None, description="Product model")
    cat_id: Optional[str] = Field(None, description="Category ID")
    price: Optional[float] = Field(None, description="Exact price")
    price_ranges: Optional[Dict[str, float]] = Field(None, description="Price range with min/max")
    backbox_grade: Optional[str] = Field(None, description="Product condition/grade")
    
    # Mobile/Electronics facets
    storage: Optional[str] = Field(None, description="Storage capacity")
    color: Optional[str] = Field(None, description="Product color")
    screen_size: Optional[str] = Field(None, description="Screen size")
    memory: Optional[str] = Field(None, description="RAM memory")
    processor: Optional[str] = Field(None, description="Processor model")
    processor_speed: Optional[str] = Field(None, description="Processor speed")
    network: Optional[List[str]] = Field(None, description="Network connectivity (4G, 5G)")
    connectivity: Optional[List[str]] = Field(None, description="Connectivity features")
    camera: Optional[str] = Field(None, description="Camera specifications")
    dual_sim: Optional[bool] = Field(None, description="Dual SIM support")
    sim_lock: Optional[bool] = Field(None, description="SIM lock status")
    battery_capacity: Optional[str] = Field(None, description="Battery capacity")
    os: Optional[str] = Field(None, description="Operating system")
    touch_bar: Optional[bool] = Field(None, description="Touch bar feature")
    touch_id: Optional[bool] = Field(None, description="Touch ID")
    face_id: Optional[bool] = Field(None, description="Face ID")
    retina: Optional[bool] = Field(None, description="Retina display")
    keyboard_type: Optional[str] = Field(None, description="Keyboard type")
    keyboard_language: Optional[str] = Field(None, description="Keyboard language")
    
    # Computing facets
    graphic_card: Optional[str] = Field(None, description="Graphics card")
    processor_type: Optional[str] = Field(None, description="Processor type")
    storage_type: Optional[str] = Field(None, description="Storage type")
    storage_ssd: Optional[str] = Field(None, description="SSD storage")
    touchscreen: Optional[bool] = Field(None, description="Touchscreen")
    webcam: Optional[bool] = Field(None, description="Webcam")
    hdmi_input: Optional[bool] = Field(None, description="HDMI input")
    hdmi_output: Optional[bool] = Field(None, description="HDMI output")
    screen_format: Optional[str] = Field(None, description="Screen format")
    screen_type: Optional[str] = Field(None, description="Screen type")
    
    # Home appliances facets
    coffee_machine_type: Optional[str] = Field(None, description="Coffee machine type")
    washing_machine_type: Optional[str] = Field(None, description="Washing machine type")
    fridge_type: Optional[str] = Field(None, description="Fridge type")
    energy_class: Optional[str] = Field(None, description="Energy class")
    capacity: Optional[str] = Field(None, description="Appliance capacity")
    power: Optional[str] = Field(None, description="Power consumption/output")
    dishwasher_type: Optional[str] = Field(None, description="Dishwasher type")
    oven_type: Optional[str] = Field(None, description="Oven type")
    hob_type: Optional[str] = Field(None, description="Hob type")
    
    # Gaming facets
    console_type: Optional[str] = Field(None, description="Console type")
    compatible_gaming_console: Optional[List[str]] = Field(None, description="Compatible consoles")
    pegi: Optional[str] = Field(None, description="PEGI rating")
    video_game_genre: Optional[str] = Field(None, description="Game genre")
    controllers_number: Optional[int] = Field(None, description="Number of controllers")
    
    # General facets
    warranty: Optional[str] = Field(None, description="Warranty period")
    deals_type: Optional[str] = Field(None, description="Deal type")
    special_offer_type: Optional[str] = Field(None, description="Special offer type")
    year_date_release: Optional[str] = Field(None, description="Release year/date")
    generation: Optional[str] = Field(None, description="Product generation")
    vintage: Optional[bool] = Field(None, description="Vintage product")
    limited_edition: Optional[bool] = Field(None, description="Limited edition")
    
    # Technical facets
    merchant_id: Optional[str] = Field(None, description="Merchant ID")
    deduplication_id: Optional[str] = Field(None, description="Deduplication ID")
    is_cheapest_listing: Optional[bool] = Field(None, description="Is cheapest listing")
    publication_state: Optional[str] = Field(None, description="Publication state")
    backbox: Optional[bool] = Field(None, description="Backbox flag")


class FacetParser:
    """Service to parse natural language queries into structured product facets"""
    
    def __init__(self, openai_api_key: str, model_name: str = "gpt-4"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.openai_api_key,
            temperature=0
        )
        self.parser = PydanticOutputParser(pydantic_object=FacetResponse)
        self.facets_schema = self._load_facets_schema()
        
    def _load_facets_schema(self) -> Dict[str, Any]:
        """Load the facets configuration schema"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "facets_config.json"
        )
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def parse_query(self, user_query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into structured product facets
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary containing extracted facets in REST API format
        """
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert product search assistant. Your task is to analyze user queries 
and extract relevant product facets/filters from their natural language request.

You must understand the user's intent and map it to the appropriate product attributes.

Here is the complete facets schema with all available fields:
{facets_schema}

Important guidelines:
- Extract ONLY the facets that are explicitly mentioned or clearly implied in the user query
- Do not invent or assume values that are not present in the query
- For price ranges, if user mentions "under X" set max to X, if "over X" set min to X
- For conditions like "new", "refurbished", "like new" use the backbox_grade field
- For colors, storage, sizes, etc., use the exact values mentioned
- For boolean fields, only set them if explicitly mentioned
- Map product categories to appropriate cat_id values
- Be intelligent about synonyms (e.g., "smartphone" = "smartphones", "laptop" = "laptops")

{format_instructions}

Respond ONLY with valid JSON matching the schema. Do not include any explanation."""),
            ("user", "{query}")
        ])
        
        # Format the prompt
        formatted_prompt = prompt.format_messages(
            facets_schema=json.dumps(self.facets_schema, indent=2),
            format_instructions=self.parser.get_format_instructions(),
            query=user_query
        )
        
        # Get response from LLM
        response = self.llm(formatted_prompt)
        
        # Parse the response
        try:
            parsed_response = self.parser.parse(response.content)
            # Convert to dict and remove None values for cleaner API response
            result = parsed_response.dict(exclude_none=True)
            return result
        except Exception as e:
            # If parsing fails, try to extract JSON manually
            try:
                # Sometimes the LLM returns JSON with extra text
                content = response.content
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                result = json.loads(content.strip())
                # Remove None values
                return {k: v for k, v in result.items() if v is not None}
            except:
                raise ValueError(f"Failed to parse LLM response: {response.content}. Error: {str(e)}")
    
    def parse_query_with_metadata(self, user_query: str) -> Dict[str, Any]:
        """
        Parse query and return with additional metadata
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary with facets and metadata
        """
        facets = self.parse_query(user_query)
        
        return {
            "query": user_query,
            "facets": facets,
            "facet_count": len(facets),
            "categories_detected": self._detect_categories(facets)
        }
    
    def _detect_categories(self, facets: Dict[str, Any]) -> List[str]:
        """Detect which facet categories are present in the parsed result"""
        categories = []
        
        mobile_fields = {'storage', 'color', 'screen_size', 'network', 'camera', 'os', 'battery_capacity'}
        computing_fields = {'graphic_card', 'processor_type', 'storage_ssd', 'touchscreen'}
        appliance_fields = {'energy_class', 'capacity', 'coffee_machine_type', 'washing_machine_type'}
        gaming_fields = {'console_type', 'pegi', 'video_game_genre', 'controllers_number'}
        
        if any(field in facets for field in mobile_fields):
            categories.append('mobile_electronics')
        if any(field in facets for field in computing_fields):
            categories.append('computing')
        if any(field in facets for field in appliance_fields):
            categories.append('home_appliances')
        if any(field in facets for field in gaming_fields):
            categories.append('gaming')
            
        return categories if categories else ['general']

