"""
FAQ Page Template

Template for generating FAQ pages with question-answer pairs.
"""

from typing import Dict, Any, List
from template_engine import TemplateDefinition, TemplateField, template_engine
from content_blocks import QuestionAnswerBlock


def create_faq_template() -> TemplateDefinition:
    """Create FAQ page template definition"""
    return TemplateDefinition(
        name="faq_page",
        description="FAQ page with categorized question-answer pairs",
        fields=[
            TemplateField(
                name="page_title",
                field_type="text",
                required=True,
                default_value="Frequently Asked Questions",
                formatting={"capitalize": True}
            ),
            TemplateField(
                name="product_name",
                field_type="text",
                required=True,
                formatting={"capitalize": True}
            ),
            TemplateField(
                name="introduction",
                field_type="text",
                required=False,
                default_value="Find answers to common questions about our product."
            ),
            TemplateField(
                name="faq_items",
                field_type="list",
                required=True,
                formatting={"max_items": 20}
            ),
            TemplateField(
                name="faq_by_category",
                field_type="structured",
                required=False
            ),
            TemplateField(
                name="categories",
                field_type="list",
                required=False,
                formatting={"unique": True}
            ),
            TemplateField(
                name="total_questions",
                field_type="number",
                required=False
            )
        ],
        dependencies=[],
        output_format="json",
        metadata={
            "page_type": "faq",
            "min_questions": 20,
            "supports_categorization": True
        }
    )


def register_faq_template() -> None:
    """Register FAQ template with the template engine"""
    template = create_faq_template()
    template_engine.register_template(template)


class FAQGenerator:
    """FAQ page generator using the template engine"""
    
    @staticmethod
    def generate_faq_page(product_data: Dict[str, Any], 
                        questions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete FAQ page"""
        
        # Extract questions
        questions = questions_data.get("questions", [])
        
        # Generate Q&A pairs (minimum 20 as required)
        faq_items = []
        target_count = 20
        selected_questions = questions[:target_count] if len(questions) >= target_count else questions
        
        for question_data in selected_questions:
            question = question_data.get("question", "")
            category = question_data.get("category", "General")
            
            # Generate answer using content block
            answer_block = QuestionAnswerBlock.generate_answer(question, product_data)
            
            faq_item = {
                "question": question,
                "answer": answer_block.content,
                "category": category,
                "priority": question_data.get("priority", 1)
            }
            faq_items.append(faq_item)

        faq_by_category: Dict[str, List[Dict[str, Any]]] = {}
        for item in faq_items:
            cat = item.get("category", "General")
            faq_by_category.setdefault(cat, []).append(
                {
                    "question": item["question"],
                    "answer": item["answer"],
                    "priority": item.get("priority", 1),
                }
            )
        
        # Prepare template data
        template_data = {
            "page_title": f"Frequently Asked Questions - {product_data.get('name', 'Product')}",
            "product_name": product_data.get("name", "Product"),
            "introduction": f"Find answers to common questions about {product_data.get('name', 'our product')}.",
            "faq_items": faq_items,
            "faq_by_category": faq_by_category,
            "categories": sorted(list(set(item["category"] for item in faq_items))),
            "total_questions": len(faq_items),
            "product_data": product_data  # For content block generation
        }
        
        # Render template
        return template_engine.render_template("faq_page", template_data)


# Register the template
register_faq_template()
