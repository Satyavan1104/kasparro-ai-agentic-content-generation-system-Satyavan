"""
Data Parser Agent

Responsible for parsing and normalizing raw product data into a clean internal model.
Single responsibility: Data transformation and validation.
"""

from typing import Dict, Any, List, Optional
import re
from agent_framework import BaseAgent, AgentResult, AgentStatus, agent_registry


class DataParserAgent(BaseAgent):
    """
    Parses raw product data into structured ProductModel.
    
    Input: Raw key-value product data
    Output: Validated ProductModel
    """
    
    def __init__(self):
        super().__init__("DataParserAgent")
        self.input_schema = {
            "type": "object",
            "properties": {
                "Product Name": {"type": "string"},
                "Concentration": {"type": "string"},
                "Skin Type": {"type": "string"},
                "Key Ingredients": {"type": "string"},
                "Benefits": {"type": "string"},
                "How to Use": {"type": "string"},
                "Side Effects": {"type": "string"},
                "Price": {"type": "string"}
            }
        }
        self.output_schema = {"type": "object"}
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input has required product name"""
        return "Product Name" in input_data and isinstance(input_data["Product Name"], str)
    
    def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Parse raw data into clean ProductModel"""
        try:
            self.status = AgentStatus.RUNNING
            
            if not self.validate_input(input_data):
                return AgentResult(
                    agent_name=self.name,
                    status=AgentStatus.FAILED,
                    errors=["Invalid input data: missing Product Name"]
                )
            
            # Extract and clean data
            product_data: Dict[str, Any] = {
                "name": self._clean_text(input_data.get("Product Name", "")) or "",
                "concentration": self._clean_text(input_data.get("Concentration")),
                "skin_types": self._parse_list(input_data.get("Skin Type")),
                "key_ingredients": self._parse_list(input_data.get("Key Ingredients")),
                "benefits": self._parse_list(input_data.get("Benefits")),
                "usage_instructions": self._clean_text(input_data.get("How to Use")),
                "side_effects": self._clean_text(input_data.get("Side Effects")),
                "price": self._clean_text(input_data.get("Price")),
                "category": self._infer_category(input_data.get("Product Name", "")),
            }
            
            self.status = AgentStatus.COMPLETED
            
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                data=product_data,
                metadata={
                    "parsed_fields": len([k for k, v in product_data.items() if v is not None and v != [] and v != ""])
                }
            )
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                errors=[f"Parsing failed: {str(e)}"]
            )
    
    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        """Clean and normalize text"""
        if not text:
            return None
        return text.strip()
    
    def _parse_list(self, text: Optional[str]) -> List[str]:
        """Parse comma-separated or hyphenated lists"""
        if not text:
            return []
        
        # Split on common separators
        items = re.split(r'[,，|]\s*|\s+and\s+|\s*[-–—]\s*', text)
        
        # Clean and filter items
        cleaned_items = []
        for item in items:
            cleaned = self._clean_text(item)
            if cleaned and len(cleaned) > 1:
                cleaned_items.append(cleaned)
        
        return cleaned_items
    
    def _infer_category(self, product_name: str) -> str:
        """Infer product category from name"""
        name_lower = product_name.lower()
        
        if "serum" in name_lower:
            return "Serum"
        elif "cream" in name_lower:
            return "Cream"
        elif "lotion" in name_lower:
            return "Lotion"
        elif "oil" in name_lower:
            return "Oil"
        else:
            return "Skincare"


# Register the agent
agent_registry.register(DataParserAgent())
