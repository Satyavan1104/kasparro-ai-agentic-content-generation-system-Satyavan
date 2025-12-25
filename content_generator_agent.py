"""
Content Generator Agent

Assembles pages using templates (FAQ, product page, comparison page).
Single responsibility: page assembly from structured models.

This agent does not parse raw product data; it expects normalized models.
"""

from typing import Any, Dict

from agent_framework import AgentResult, AgentStatus, BaseAgent, agent_registry

from templates.comparison_template import ComparisonPageGenerator
from templates.faq_template import FAQGenerator
from templates.product_template import ProductPageGenerator


class ContentGeneratorAgent(BaseAgent):
     """Generate structured pages as JSON objects (not files)."""

     def __init__(self):
         super().__init__("ContentGeneratorAgent")
         self.input_schema = {
             "type": "object",
             "properties": {
                 "product_a": {"type": "object"},
                 "questions": {"type": "object"},
                 "product_b": {"type": "object"},
             },
             "required": ["product_a", "questions", "product_b"],
         }
         self.output_schema = {"type": "object"}

     def validate_input(self, input_data: Dict[str, Any]) -> bool:
         return (
             isinstance(input_data.get("product_a"), dict)
             and isinstance(input_data.get("product_b"), dict)
             and isinstance(input_data.get("questions"), dict)
         )

     def process(self, input_data: Dict[str, Any]) -> AgentResult:
         try:
             self.status = AgentStatus.RUNNING

             if not self.validate_input(input_data):
                 return AgentResult(
                     agent_name=self.name,
                     status=AgentStatus.FAILED,
                     errors=["Invalid input: expected product_a, product_b, questions"],
                 )

             product_a = input_data["product_a"]
             product_b = input_data["product_b"]
             questions = input_data["questions"]

             faq_page = FAQGenerator.generate_faq_page(product_a, questions)
             product_page = ProductPageGenerator.generate_product_page(product_a)
             comparison_page = ComparisonPageGenerator.generate_comparison_page(product_a, product_b)

             self.status = AgentStatus.COMPLETED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.COMPLETED,
                 data={
                     "faq_page": faq_page,
                     "product_page": product_page,
                     "comparison_page": comparison_page,
                 },
                 metadata={"pages": 3},
             )

         except Exception as e:
             self.status = AgentStatus.FAILED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.FAILED,
                 errors=[f"Content generation failed: {str(e)}"],
             )


agent_registry.register(ContentGeneratorAgent())
