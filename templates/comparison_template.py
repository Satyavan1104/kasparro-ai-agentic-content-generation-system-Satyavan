"""
Comparison Page Template

Template for generating product comparison pages.
"""

from typing import Dict, Any, List
from template_engine import TemplateDefinition, TemplateField, template_engine


def create_comparison_template() -> TemplateDefinition:
    """Create comparison page template definition"""
    return TemplateDefinition(
        name="comparison_page",
        description="Product comparison page between two products",
        fields=[
            TemplateField(
                name="page_title",
                field_type="text",
                required=True,
                formatting={"capitalize": True}
            ),
            TemplateField(
                name="introduction",
                field_type="text",
                required=True
            ),
            TemplateField(
                name="product_a",
                field_type="structured",
                required=True
            ),
            TemplateField(
                name="product_b",
                field_type="structured",
                required=True
            ),
            TemplateField(
                name="comparison_ingredients",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="comparison_benefits",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="comparison_prices",
                field_type="block",
                required=True
            ),
            TemplateField(
                name="key_differences",
                field_type="list",
                required=True,
                formatting={"max_items": 5}
            ),
            TemplateField(
                name="recommendation",
                field_type="text",
                required=False
            ),
            TemplateField(
                name="comparison_summary",
                field_type="structured",
                required=True
            )
        ],
        dependencies=["comparison_ingredients", "comparison_benefits", "comparison_prices"],
        output_format="json",
        metadata={
            "page_type": "comparison",
            "requires_two_products": True,
            "supports_side_by_side": True
        }
    )


def register_comparison_template() -> None:
    """Register comparison template with the template engine"""
    template = create_comparison_template()
    template_engine.register_template(template)


class ComparisonPageGenerator:
    """Comparison page generator using the template engine"""
    
    @staticmethod
    def generate_comparison_page(product_a: Dict[str, Any], 
                              product_b: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete comparison page"""
        
        # Generate introduction
        introduction = ComparisonPageGenerator._generate_introduction(product_a, product_b)
        
        # Generate key differences
        key_differences = ComparisonPageGenerator._generate_key_differences(product_a, product_b)
        
        # Generate recommendation
        recommendation = ComparisonPageGenerator._generate_recommendation(product_a, product_b)
        
        # Generate comparison summary
        comparison_summary = ComparisonPageGenerator._generate_summary(product_a, product_b)
        
        # Prepare template data
        template_data = {
            "page_title": f"{product_a.get('name', 'Product A')} vs {product_b.get('name', 'Product B')} Comparison",
            "introduction": introduction,
            "product_a": ComparisonPageGenerator._prepare_product_summary(product_a),
            "product_b": ComparisonPageGenerator._prepare_product_summary(product_b),
            "key_differences": key_differences,
            "recommendation": recommendation,
            "comparison_summary": comparison_summary,
            "product_a_full": product_a,
            "product_b_full": product_b,
        }
        
        # Render template
        return template_engine.render_template("comparison_page", template_data)
    
    @staticmethod
    def _generate_introduction(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Generate comparison introduction"""
        name_a = product_a.get("name", "Product A")
        name_b = product_b.get("name", "Product B")
        
        intro = f"Compare {name_a} and {name_b} based on the provided product data."
        
        # Add category context
        category_a = product_a.get("category", "skincare")
        category_b = product_b.get("category", "skincare")
        
        if category_a == category_b:
            intro += f" Both are {category_a.lower()} products with distinct formulations and benefits."
        
        return intro
    
    @staticmethod
    def _prepare_product_summary(product: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare product summary for comparison"""
        return {
            "name": product.get("name", "Unknown Product"),
            "category": product.get("category", "Skincare"),
            "price": product.get("price", "Price not available"),
            "key_ingredients": product.get("key_ingredients", []),
            "benefits": product.get("benefits", []),
            "skin_types": product.get("skin_types", []),
            "concentration": product.get("concentration")
        }
    
    @staticmethod
    def _generate_key_differences(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> List[str]:
        """Generate key differences between products"""
        differences = []
        
        # Ingredient differences
        ingredients_a = set(product_a.get("key_ingredients", []))
        ingredients_b = set(product_b.get("key_ingredients", []))
        
        unique_a = ingredients_a - ingredients_b
        unique_b = ingredients_b - ingredients_a
        
        if unique_a:
            differences.append(f"{product_a['name']} contains {', '.join(unique_a)}")
        
        if unique_b:
            differences.append(f"{product_b['name']} contains {', '.join(unique_b)}")
        
        # Benefit differences
        benefits_a = set(product_a.get("benefits", []))
        benefits_b = set(product_b.get("benefits", []))
        
        unique_benefits_a = benefits_a - benefits_b
        unique_benefits_b = benefits_b - benefits_a
        
        if unique_benefits_a:
            differences.append(f"{product_a['name']} focuses on {', '.join(unique_benefits_a)}")
        
        if unique_benefits_b:
            differences.append(f"{product_b['name']} emphasizes {', '.join(unique_benefits_b)}")
        
        # Price difference
        price_a = product_a.get("price")
        price_b = product_b.get("price")
        
        if price_a and price_b and price_a != price_b:
            differences.append(f"Price difference: {price_a} vs {price_b}")
        
        # Concentration difference
        conc_a = product_a.get("concentration")
        conc_b = product_b.get("concentration")
        
        if conc_a and conc_b and conc_a != conc_b:
            differences.append(f"Different concentrations: {conc_a} vs {conc_b}")
        
        return differences[:5]  # Limit to 5 key differences
    
    @staticmethod
    def _generate_recommendation(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Generate recommendation based on comparison"""
        name_a = product_a.get("name", "Product A")
        name_b = product_b.get("name", "Product B")
        
        # Simple recommendation logic based on benefits and ingredients
        benefits_a = product_a.get("benefits", [])
        benefits_b = product_b.get("benefits", [])
        
        if len(benefits_a) > len(benefits_b):
            recommendation = f"Choose {name_a} if you prefer the benefit set listed for it."
        elif len(benefits_b) > len(benefits_a):
            recommendation = f"Choose {name_b} if you prefer the benefit set listed for it."
        else:
            # Check for specific benefit types
            if "brightening" in [b.lower() for b in benefits_a]:
                recommendation = f"Choose {name_a} for brightening and dark spot correction."
            elif "brightening" in [b.lower() for b in benefits_b]:
                recommendation = f"Choose {name_b} for brightening and dark spot correction."
            else:
                recommendation = f"Both {name_a} and {name_b} list similar amounts of benefit information. Choose based on your preferences and budget."
        
        return recommendation
    
    @staticmethod
    def _generate_summary(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison summary"""
        return {
            "winner": ComparisonPageGenerator._determine_winner(product_a, product_b),
            "best_value": ComparisonPageGenerator._determine_best_value(product_a, product_b),
            "best_for_benefits": ComparisonPageGenerator._determine_best_for_benefits(product_a, product_b),
            "best_for_sensitive": ComparisonPageGenerator._determine_best_for_sensitive(product_a, product_b),
            "overall_score": {
                product_a.get("name", "Product A"): ComparisonPageGenerator._calculate_score(product_a),
                product_b.get("name", "Product B"): ComparisonPageGenerator._calculate_score(product_b)
            }
        }
    
    @staticmethod
    def _determine_winner(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Determine overall winner"""
        score_a = ComparisonPageGenerator._calculate_score(product_a)
        score_b = ComparisonPageGenerator._calculate_score(product_b)
        
        if score_a > score_b:
            return product_a.get("name", "Product A")
        elif score_b > score_a:
            return product_b.get("name", "Product B")
        else:
            return "Both products are equally matched"
    
    @staticmethod
    def _determine_best_value(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Determine best value based on price vs benefits"""
        # Simple value calculation: benefits count / price indicator
        benefits_a = len(product_a.get("benefits", []))
        benefits_b = len(product_b.get("benefits", []))
        
        # Extract numeric price for comparison (simplified)
        price_a = product_a.get("price", "999999")
        price_b = product_b.get("price", "999999")
        
        # Extract numbers from price strings
        import re
        num_a = int(re.findall(r'\d+', str(price_a))[0]) if re.findall(r'\d+', str(price_a)) else 999999
        num_b = int(re.findall(r'\d+', str(price_b))[0]) if re.findall(r'\d+', str(price_b)) else 999999
        
        value_a = benefits_a / max(num_a, 1)
        value_b = benefits_b / max(num_b, 1)
        
        if value_a > value_b:
            return product_a.get("name", "Product A")
        else:
            return product_b.get("name", "Product B")
    
    @staticmethod
    def _determine_best_for_benefits(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Determine best for benefits"""
        benefits_a = len(product_a.get("benefits", []))
        benefits_b = len(product_b.get("benefits", []))
        
        return product_a.get("name", "Product A") if benefits_a >= benefits_b else product_b.get("name", "Product B")
    
    @staticmethod
    def _determine_best_for_sensitive(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Determine best for sensitive skin"""
        # Check for side effects warnings
        side_effects_a = product_a.get("side_effects", "")
        side_effects_b = product_b.get("side_effects", "")
        
        if "sensitive" in str(side_effects_a).lower():
            return product_b.get("name", "Product B")
        elif "sensitive" in str(side_effects_b).lower():
            return product_a.get("name", "Product A")
        else:
            return "Not specified"
    
    @staticmethod
    def _calculate_score(product: Dict[str, Any]) -> int:
        """Calculate overall product score"""
        score = 0
        
        # Benefits score
        benefits = product.get("benefits", [])
        score += len(benefits) * 10
        
        # Ingredients score
        ingredients = product.get("key_ingredients", [])
        score += len(ingredients) * 5
        
        # Skin type compatibility score
        skin_types = product.get("skin_types", [])
        score += len(skin_types) * 3
        
        # Has usage instructions
        if product.get("usage_instructions"):
            score += 5
        
        # Has concentration info
        if product.get("concentration"):
            score += 3
        
        return score


# Register the template
register_comparison_template()
