"""
Reusable Content Logic Blocks

Modular functions that apply rules to transform data into copy.
These blocks are reusable across different templates and agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ContentBlock:
    """Base content block structure"""

    block_type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BenefitsBlock:
    """Generates benefits-focused content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any]) -> ContentBlock:
        """Generate benefits description block"""
        benefits = product_data.get("benefits", [])
        product_name = product_data.get("name", "this product")
        
        if not benefits:
            content = f"Benefits for {product_name} are not provided."
        else:
            benefit_text = ", ".join(benefits[:-1]) + f" and {benefits[-1]}" if len(benefits) > 1 else benefits[0]
            content = f"{product_name} delivers powerful benefits including {benefit_text}."
        
        return ContentBlock(
            block_type="benefits",
            content=content,
            metadata={"benefit_count": len(benefits)}
        )


class UsageBlock:
    """Generates usage instructions content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any]) -> ContentBlock:
        """Generate usage instructions block"""
        usage = product_data.get("usage_instructions")
        product_name = product_data.get("name", "this product")
        
        if usage:
            content = f"How to use {product_name}: {usage}"
        else:
            content = f"Usage instructions for {product_name} are not provided."
        
        return ContentBlock(
            block_type="usage",
            content=content,
            metadata={"has_instructions": bool(usage)}
        )


class IngredientsBlock:
    """Generates ingredients-focused content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any], detailed: bool = False) -> ContentBlock:
        """Generate ingredients description block"""
        ingredients = product_data.get("key_ingredients", [])
        concentration = product_data.get("concentration")
        product_name = product_data.get("name", "this product")
        
        if not ingredients:
            content = f"Key ingredients for {product_name} are not provided."
        else:
            if detailed and len(ingredients) > 1:
                ingredient_text = f"key ingredients {', '.join(ingredients[:-1])} and {ingredients[-1]}"
            else:
                ingredient_text = f"{' and '.join(ingredients)}" if len(ingredients) > 1 else ingredients[0]
            
            content = f"{product_name} features {ingredient_text}"
            
            if concentration:
                content += f" at {concentration} concentration"
            
            content += "."
        
        return ContentBlock(
            block_type="ingredients",
            content=content,
            metadata={"ingredient_count": len(ingredients), "detailed": detailed}
        )


class SafetyBlock:
    """Generates safety and side effects content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any]) -> ContentBlock:
        """Generate safety information block"""
        side_effects = product_data.get("side_effects")
        product_name = product_data.get("name", "this product")
        
        if side_effects:
            content = f"Safety information: {side_effects}"
        else:
            content = f"Side effects information for {product_name} is not provided."
        
        return ContentBlock(
            block_type="safety",
            content=content,
            metadata={"has_warnings": bool(side_effects)}
        )


class SkinTypeBlock:
    """Generates skin type compatibility content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any]) -> ContentBlock:
        """Generate skin type compatibility block"""
        skin_types = product_data.get("skin_types", [])
        product_name = product_data.get("name", "this product")
        
        if not skin_types:
            content = f"Suitable skin types for {product_name} are not specified."
        else:
            if len(skin_types) > 1:
                skin_text = ", ".join(skin_types[:-1]) + f" and {skin_types[-1]}"
                content = f"{product_name} is specially formulated for {skin_text} skin types."
            else:
                content = f"{product_name} is ideal for {skin_types[0]} skin."
        
        return ContentBlock(
            block_type="skin_type",
            content=content,
            metadata={"skin_type_count": len(skin_types)}
        )


class PriceBlock:
    """Generates pricing information content"""
    
    @staticmethod
    def generate(product_data: Dict[str, Any]) -> ContentBlock:
        """Generate pricing information block"""
        price = product_data.get("price")
        product_name = product_data.get("name", "this product")
        
        if price:
            content = f"{product_name} is priced at {price}."
        else:
            content = f"Price for {product_name} is not provided."
        
        return ContentBlock(
            block_type="price",
            content=content,
            metadata={"has_price": bool(price)}
        )


class ComparisonBlock:
    """Generates comparison-focused content"""
    
    @staticmethod
    def compare_ingredients(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> ContentBlock:
        """Compare ingredients between two products"""
        ingredients_a = set(product_a.get("key_ingredients", []))
        ingredients_b = set(product_b.get("key_ingredients", []))
        
        common = ingredients_a.intersection(ingredients_b)
        unique_a = ingredients_a - ingredients_b
        unique_b = ingredients_b - ingredients_a
        
        content_parts = []
        
        if common:
            common_text = ", ".join(common)
            content_parts.append(f"Both products contain {common_text}")
        
        if unique_a:
            unique_a_text = ", ".join(unique_a)
            content_parts.append(f"{product_a['name']} uniquely features {unique_a_text}")
        
        if unique_b:
            unique_b_text = ", ".join(unique_b)
            content_parts.append(f"{product_b['name']} uniquely features {unique_b_text}")
        
        content = ". ".join(content_parts) + "." if content_parts else "Both products have distinct ingredient formulations."
        
        return ContentBlock(
            block_type="ingredient_comparison",
            content=content,
            metadata={
                "common_ingredients": len(common),
                "unique_a": len(unique_a),
                "unique_b": len(unique_b)
            }
        )
    
    @staticmethod
    def compare_benefits(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> ContentBlock:
        """Compare benefits between two products"""
        benefits_a = set(product_a.get("benefits", []))
        benefits_b = set(product_b.get("benefits", []))
        
        common = benefits_a.intersection(benefits_b)
        unique_a = benefits_a - benefits_b
        unique_b = benefits_b - benefits_a
        
        content_parts = []
        
        if common:
            common_text = ", ".join(common)
            content_parts.append(f"Both products offer {common_text}")
        
        if unique_a:
            unique_a_text = ", ".join(unique_a)
            content_parts.append(f"{product_a['name']} specifically provides {unique_a_text}")
        
        if unique_b:
            unique_b_text = ", ".join(unique_b)
            content_parts.append(f"{product_b['name']} focuses on {unique_b_text}")
        
        content = ". ".join(content_parts) + "." if content_parts else "Each product offers unique benefits."
        
        return ContentBlock(
            block_type="benefit_comparison",
            content=content,
            metadata={
                "common_benefits": len(common),
                "unique_a": len(unique_a),
                "unique_b": len(unique_b)
            }
        )
    
    @staticmethod
    def compare_prices(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> ContentBlock:
        """Compare prices between two products"""
        price_a = product_a.get("price", "unspecified")
        price_b = product_b.get("price", "unspecified")
        
        content = f"Price comparison: {product_a['name']} ({price_a}) vs {product_b['name']} ({price_b})."
        
        return ContentBlock(
            block_type="price_comparison",
            content=content,
            metadata={"both_priced": bool(product_a.get("price") and product_b.get("price"))}
        )


class QuestionAnswerBlock:
    """Generates question and answer pairs"""
    
    @staticmethod
    def generate_answer(question: str, product_data: Dict[str, Any]) -> ContentBlock:
        """Generate answer for a specific question based on product data"""
        question_lower = question.lower()
        product_name = product_data.get("name", "this product")
        
        # Answer generation logic based on question type
        if "price" in question_lower:
            price = product_data.get("price")
            answer = f"{product_name} costs {price}." if price else f"Price for {product_name} is not provided."

        elif "what is" in question_lower or "what are" in question_lower:
            if "ingredient" in question_lower:
                ingredients = ", ".join(product_data.get("key_ingredients", []))
                answer = f"{product_name} contains {ingredients}." if ingredients else f"Key ingredients for {product_name} are not provided."
            elif "benefit" in question_lower:
                benefits = ", ".join(product_data.get("benefits", []))
                answer = f"{product_name} provides {benefits}." if benefits else f"Benefits for {product_name} are not provided."
            else:
                category = product_data.get("category")
                if category:
                    answer = f"{product_name} is a {category} product."
                else:
                    answer = f"{product_name} is a product."
        
        elif "how to use" in question_lower or "apply" in question_lower:
            usage = product_data.get("usage_instructions")
            answer = usage if usage else f"Usage instructions for {product_name} are not provided."
        
        elif "side effect" in question_lower or "safe" in question_lower:
            side_effects = product_data.get("side_effects")
            answer = side_effects if side_effects else f"Side effects information for {product_name} is not provided."
        
        elif "skin type" in question_lower or "suitable" in question_lower:
            skin_types = product_data.get("skin_types", [])
            if skin_types:
                skin_text = ", ".join(skin_types)
                answer = f"{product_name} is suitable for {skin_text} skin types."
            else:
                answer = f"Suitable skin types for {product_name} are not specified."
        
        else:
            # Generic answer for other questions
            answer = f"The available product data does not specify this detail for {product_name}."
        
        return ContentBlock(
            block_type="qa_answer",
            content=answer,
            metadata={"question_type": QuestionAnswerBlock._classify_question(question)}
        )
    
    @staticmethod
    def _classify_question(question: str) -> str:
        """Classify question type for answer generation"""
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ["what is", "what are"]):
            return "informational"
        elif any(keyword in question_lower for keyword in ["how to", "apply", "use"]):
            return "usage"
        elif any(keyword in question_lower for keyword in ["safe", "side effect", "precaution"]):
            return "safety"
        elif any(keyword in question_lower for keyword in ["skin type", "suitable"]):
            return "skin_type"
        elif "price" in question_lower:
            return "purchase"
        else:
            return "general"


# Content block registry for easy access
CONTENT_BLOCKS = {
    "benefits": BenefitsBlock,
    "usage": UsageBlock,
    "ingredients": IngredientsBlock,
    "safety": SafetyBlock,
    "skin_type": SkinTypeBlock,
    "price": PriceBlock,
    "comparison": ComparisonBlock,
    "qa": QuestionAnswerBlock
}
