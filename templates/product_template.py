"""
Product Page Template

Template for generating comprehensive product description pages.
"""

from typing import Dict, Any, List
from template_engine import TemplateDefinition, TemplateField, template_engine


def create_product_template() -> TemplateDefinition:
    """Create product page template definition"""
    return TemplateDefinition(
        name="product_page",
        description="Comprehensive product description page",
        fields=[
            TemplateField(
                name="product_name",
                field_type="text",
                required=True,
                formatting={"capitalize": True}
            ),
            TemplateField(
                name="tagline",
                field_type="text",
                required=False,
                default_value="Skincare product"
            ),
            TemplateField(
                name="category",
                field_type="text",
                required=False,
                formatting={"capitalize": True}
            ),
            TemplateField(
                name="description",
                field_type="text",
                required=True
            ),
            TemplateField(
                name="key_features",
                field_type="list",
                required=True,
                formatting={"max_items": 6}
            ),
            TemplateField(
                name="ingredients",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="benefits",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="usage",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="safety",
                field_type="block",
                required=False
            ),
            TemplateField(
                name="skin_type",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="price",
                field_type="block",
                required=True
            )
        ],
        dependencies=["benefits", "usage", "ingredients", "safety", "skin_type", "price"],
        output_format="json",
        metadata={
            "page_type": "product",
            "requires_full_product_data": True,
            "supports_rich_content": True
        }
    )


def register_product_template() -> None:
    """Register product template with the template engine"""
    template = create_product_template()
    template_engine.register_template(template)


class ProductPageGenerator:
    """Product page generator using the template engine"""
    
    @staticmethod
    def generate_product_page(product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete product page"""
        
        # Generate product description
        description = ProductPageGenerator._generate_description(product_data)
        
        # Generate key features
        key_features = ProductPageGenerator._generate_key_features(product_data)
        
        # Prepare template data
        template_data = {
            "product_name": product_data.get("name", "Product"),
            "tagline": ProductPageGenerator._generate_tagline(product_data),
            "category": product_data.get("category", "Skincare"),
            "description": description,
            "key_features": key_features,
            "product_data": product_data  # For content block generation
        }
        
        # Render template
        return template_engine.render_template("product_page", template_data)
    
    @staticmethod
    def _generate_description(product_data: Dict[str, Any]) -> str:
        """Generate product description"""
        name = product_data.get("name", "This product")
        benefits = product_data.get("benefits", [])
        skin_types = product_data.get("skin_types", [])
        
        description = f"{name} is a {product_data.get('category', 'skincare').lower()} product"
        
        if benefits:
            benefit_text = ", ".join(benefits[:2])
            description += f" with listed benefits including {benefit_text}"
        
        if skin_types:
            if len(skin_types) > 1:
                skin_text = " and ".join(skin_types[:2])
            else:
                skin_text = skin_types[0]
            description += f", listed as suitable for {skin_text} skin"
        
        description += "."
        
        # Add ingredient highlight
        ingredients = product_data.get("key_ingredients", [])
        if ingredients:
            main_ingredient = ingredients[0]
            description += f" It includes {main_ingredient} as a key ingredient,"
            
            if product_data.get("concentration"):
                description += f" delivered at {product_data['concentration']} concentration,"
            
            if benefits:
                description += f" and is described as supporting {', '.join(benefits)}."
            else:
                description += "."
        
        return description
    
    @staticmethod
    def _generate_tagline(product_data: Dict[str, Any]) -> str:
        """Generate product tagline"""
        benefits = product_data.get("benefits", [])
        ingredients = product_data.get("key_ingredients", [])
        
        if benefits:
            main_benefit = benefits[0]
            return f"Benefit focus: {main_benefit}"
        elif ingredients:
            main_ingredient = ingredients[0]
            return f"Featuring {main_ingredient}"
        else:
            return "Skincare product"
    
    @staticmethod
    def _generate_key_features(product_data: Dict[str, Any]) -> List[str]:
        """Generate key features list"""
        features = []
        
        # Add benefit-based features
        benefits = product_data.get("benefits", [])
        for benefit in benefits[:3]:
            features.append(f"Supports {benefit.lower()}")
        
        # Add ingredient-based features
        ingredients = product_data.get("key_ingredients", [])
        if ingredients:
            features.append(f"Contains {', '.join(ingredients[:2])}")
        
        # Add concentration if available
        if product_data.get("concentration"):
            features.append(f"Concentration: {product_data['concentration']}")
        
        # Add skin type feature
        skin_types = product_data.get("skin_types", [])
        if skin_types:
            if len(skin_types) > 1:
                features.append("Suitable for oily and combination skin")
            else:
                features.append(f"Suitable for {skin_types[0]} skin")
        
        return features[:6]  # Limit to 6 features


# Register the template
register_product_template()
