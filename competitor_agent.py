"""
Competitor Product Agent

Creates a structured fictional Product B for comparison.
Single responsibility: generate a competitor product object (no external research).

NOTE: Product B is fictional by assignment requirement.
"""

from typing import Any, Dict

from agent_framework import AgentResult, AgentStatus, BaseAgent, agent_registry


class CompetitorAgent(BaseAgent):
     """Generate a fictional competitor product with the same internal schema."""

     def __init__(self):
         super().__init__("CompetitorAgent")
         self.input_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
         self.output_schema = {"type": "object"}

     def validate_input(self, input_data: Dict[str, Any]) -> bool:
         return "name" in input_data and isinstance(input_data["name"], str)

     def process(self, input_data: Dict[str, Any]) -> AgentResult:
         try:
             self.status = AgentStatus.RUNNING

             if not self.validate_input(input_data):
                 return AgentResult(
                     agent_name=self.name,
                     status=AgentStatus.FAILED,
                     errors=["Invalid input: expected parsed product data with 'name'"]
                 )

             competitor = {
                 "name": "RadianceMax Niacinamide Serum",
                 "concentration": "5% Niacinamide",
                 "skin_types": ["Oily", "Combination"],
                 "key_ingredients": ["Niacinamide", "Peptides"],
                 "benefits": ["Oil control", "Evens skin tone"],
                 "usage_instructions": "Apply 2–3 drops in the morning and evening.",
                 "side_effects": "May cause mild dryness for some users.",
                 "price": "₹749",
                 "category": "Serum",
                 "fictional": True,
             }

             self.status = AgentStatus.COMPLETED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.COMPLETED,
                 data={"product_b": competitor},
                 metadata={"generated": True},
             )

         except Exception as e:
             self.status = AgentStatus.FAILED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.FAILED,
                 errors=[f"Competitor generation failed: {str(e)}"],
             )


agent_registry.register(CompetitorAgent())
