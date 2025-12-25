"""
Template Engine

Custom template system for structured content generation.
Templates define fields, rules, formatting, and dependencies on content blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from abc import ABC, abstractmethod
from content_blocks import ContentBlock, CONTENT_BLOCKS


@dataclass
class TemplateField:
    """Individual template field definition"""

    name: str
    field_type: str
    required: bool = True
    default_value: Optional[Any] = None
    validation_rules: Optional[List[str]] = None
    formatting: Optional[Dict[str, Any]] = None


@dataclass
class TemplateDefinition:
    """Complete template definition"""

    name: str
    description: str
    fields: List[TemplateField]
    dependencies: Optional[List[str]] = None
    output_format: str = "json"
    metadata: Optional[Dict[str, Any]] = None


class TemplateRenderer(ABC):
    """Abstract base class for template renderers"""
    
    @abstractmethod
    def render(self, template: TemplateDefinition, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render template with provided data"""
        pass


class JSONTemplateRenderer(TemplateRenderer):
    """JSON template renderer"""
    
    def render(self, template: TemplateDefinition, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render template as structured JSON"""
        result = {
            "template_name": template.name,
            "metadata": template.metadata or {},
            "content": {}
        }
        
        # Process each field
        for field in template.fields:
            field_value = self._process_field(field, data)
            if field_value is not None or not field.required:
                result["content"][field.name] = field_value
        
        return result
    
    def _process_field(self, field: TemplateField, data: Dict[str, Any]) -> Any:
        """Process individual template field"""
        # Get field value from data
        raw_value = data.get(field.name, field.default_value)
        
        if raw_value is None:
            return None
        
        # Apply field type processing
        if field.field_type == "text":
            return self._process_text_field(raw_value, field.formatting)
        elif field.field_type == "list":
            return self._process_list_field(raw_value, field.formatting)
        elif field.field_type == "block":
            return self._process_block_field(raw_value, field.formatting)
        elif field.field_type == "structured":
            return self._process_structured_field(raw_value, field.formatting)
        else:
            return raw_value
    
    def _process_text_field(self, value: Any, formatting: Optional[Dict[str, Any]]) -> str:
        """Process text field with formatting"""
        if not isinstance(value, str):
            value = str(value)
        
        if formatting:
            # Apply text formatting rules
            if formatting.get("capitalize"):
                value = value.capitalize()
            if formatting.get("uppercase"):
                value = value.upper()
            if formatting.get("lowercase"):
                value = value.lower()
            if formatting.get("max_length"):
                value = value[:formatting["max_length"]]
        
        return value
    
    def _process_list_field(self, value: Any, formatting: Optional[Dict[str, Any]]) -> List[Any]:
        """Process list field with formatting"""
        if not isinstance(value, list):
            if isinstance(value, str):
                # Split string into list
                value = [item.strip() for item in value.split(",") if item.strip()]
            else:
                value = [value]
        
        if formatting:
            # Apply list formatting
            if formatting.get("max_items"):
                value = value[:formatting["max_items"]]
            if formatting.get("unique"):
                value = list(dict.fromkeys(value))  # Remove duplicates while preserving order
        
        return value
    
    def _process_block_field(self, value: Any, formatting: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process content block field"""
        if isinstance(value, ContentBlock):
            result = {
                "type": value.block_type,
                "content": value.content,
                "metadata": value.metadata or {}
            }
        elif isinstance(value, dict):
            result = value
        else:
            result = {"content": str(value), "type": "text"}
        
        if formatting:
            # Apply block formatting
            if formatting.get("include_metadata") is False:
                result.pop("metadata", None)
            if formatting.get("content_only"):
                return result["content"]
        
        return result
    
    def _process_structured_field(self, value: Any, formatting: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process structured field (nested objects)"""
        if isinstance(value, dict):
            return value
        else:
            return {"value": value}


class TemplateEngine:
    """Main template engine for content generation"""
    
    def __init__(self):
        self.templates: Dict[str, TemplateDefinition] = {}
        self.renderers: Dict[str, TemplateRenderer] = {
            "json": JSONTemplateRenderer()
        }
        self.block_generators: Dict[str, Callable] = {}
        
        # Register default content block generators
        self._register_default_blocks()
    
    def register_template(self, template: TemplateDefinition) -> None:
        """Register a new template"""
        self.templates[template.name] = template
    
    def register_renderer(self, format_name: str, renderer: TemplateRenderer) -> None:
        """Register a new renderer"""
        self.renderers[format_name] = renderer
    
    def register_block_generator(self, block_type: str, generator: Callable) -> None:
        """Register a content block generator"""
        self.block_generators[block_type] = generator
    
    def render_template(self, template_name: str, data: Dict[str, Any], 
                       output_format: str = "json") -> Dict[str, Any]:
        """Render a template with provided data"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        
        # Check dependencies
        if template.dependencies:
            self._check_dependencies(template.dependencies, data)
        
        # Generate content blocks if needed
        enriched_data = self._generate_content_blocks(template, data)
        
        # Get appropriate renderer
        if output_format not in self.renderers:
            raise ValueError(f"Renderer for format '{output_format}' not found")
        
        renderer = self.renderers[output_format]
        
        # Render template
        return renderer.render(template, enriched_data)
    
    def list_templates(self) -> List[str]:
        """List all registered template names"""
        return list(self.templates.keys())
    
    def get_template(self, template_name: str) -> Optional[TemplateDefinition]:
        """Get template definition by name"""
        return self.templates.get(template_name)
    
    def _register_default_blocks(self) -> None:
        """Register default content block generators"""
        for block_name, block_class in CONTENT_BLOCKS.items():
            if hasattr(block_class, 'generate'):
                self.block_generators[block_name] = block_class.generate
            elif hasattr(block_class, 'compare_ingredients'):
                self.block_generators[f"{block_name}_ingredients"] = block_class.compare_ingredients
                self.block_generators[f"{block_name}_benefits"] = block_class.compare_benefits
                self.block_generators[f"{block_name}_prices"] = block_class.compare_prices
            elif hasattr(block_class, 'generate_answer'):
                self.block_generators[f"{block_name}_answer"] = block_class.generate_answer
    
    def _check_dependencies(self, dependencies: List[str], data: Dict[str, Any]) -> None:
        """Check if all dependencies are satisfied"""
        missing_deps = []
        
        for dep in dependencies:
            if dep not in data and dep not in self.block_generators:
                missing_deps.append(dep)
        
        if missing_deps:
            raise ValueError(f"Missing dependencies: {missing_deps}")
    
    def _generate_content_blocks(self, template: TemplateDefinition, 
                               data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content blocks for template"""
        enriched_data = data.copy()
        
        if not template.dependencies:
            return enriched_data
        
        # Generate each dependency
        for dep in template.dependencies:
            if dep not in enriched_data and dep in self.block_generators:
                try:
                    generator = self.block_generators[dep]
                    
                    # Handle different generator signatures
                    if dep.startswith("comparison"):
                        # Comparison blocks need two products
                        product_a = data.get("product_a_full") or data.get("product_a")
                        product_b = data.get("product_b_full") or data.get("product_b")
                        if isinstance(product_a, dict) and isinstance(product_b, dict):
                            if "ingredients" in dep:
                                block = generator(product_a, product_b)
                            elif "benefits" in dep:
                                block = generator(product_a, product_b)
                            elif "prices" in dep:
                                block = generator(product_a, product_b)
                            else:
                                continue
                            enriched_data[dep] = block
                    elif dep.endswith("_answer"):
                        # QA blocks need question and product data
                        if "question" in data and "product_data" in data:
                            block = generator(data["question"], data["product_data"])
                            enriched_data[dep] = block
                    else:
                        # Regular blocks need product data
                        if "product_data" in data:
                            block = generator(data["product_data"])
                            enriched_data[dep] = block
                
                except Exception as e:
                    # Log error but continue processing
                    print(f"Warning: Failed to generate block '{dep}': {e}")
        
        return enriched_data


# Global template engine instance
template_engine = TemplateEngine()
