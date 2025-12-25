"""
JSON Output Agent

Writes machine-readable JSON pages to disk.
Single responsibility: persist JSON objects as files.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from agent_framework import AgentResult, AgentStatus, BaseAgent, agent_registry


class JsonOutputAgent(BaseAgent):
     """Write JSON page objects to files."""

     def __init__(self):
         super().__init__("JsonOutputAgent")
         self.input_schema = {
             "type": "object",
             "properties": {
                 "output_dir": {"type": "string"},
                 "pages": {"type": "object"},
             },
             "required": ["output_dir", "pages"],
         }
         self.output_schema = {"type": "object"}

     def validate_input(self, input_data: Dict[str, Any]) -> bool:
         return isinstance(input_data.get("output_dir"), str) and isinstance(input_data.get("pages"), dict)

     def process(self, input_data: Dict[str, Any]) -> AgentResult:
         try:
             self.status = AgentStatus.RUNNING

             if not self.validate_input(input_data):
                 return AgentResult(
                     agent_name=self.name,
                     status=AgentStatus.FAILED,
                     errors=["Invalid input: expected output_dir and pages dict"],
                 )

             out_dir = input_data["output_dir"]
             pages = input_data["pages"]
             graph = input_data.get("graph")

             os.makedirs(out_dir, exist_ok=True)

             file_map = {
                 "faq_page": "faq.json",
                 "product_page": "product_page.json",
                 "comparison_page": "comparison_page.json",
             }

             written = {}
             for key, filename in file_map.items():
                 if key not in pages:
                     continue
                 path = os.path.join(out_dir, filename)
                 with open(path, "w", encoding="utf-8") as f:
                     json.dump(pages[key], f, ensure_ascii=False, indent=2)
                 written[key] = path

             if graph is not None:
                 graph_path = os.path.join(out_dir, "graph.json")
                 with open(graph_path, "w", encoding="utf-8") as f:
                     json.dump(graph, f, ensure_ascii=False, indent=2)
                 written["graph"] = graph_path

             self.status = AgentStatus.COMPLETED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.COMPLETED,
                 data={"written_files": written},
                 metadata={"count": len(written)},
             )

         except Exception as e:
             self.status = AgentStatus.FAILED
             return AgentResult(
                 agent_name=self.name,
                 status=AgentStatus.FAILED,
                 errors=[f"JSON write failed: {str(e)}"],
             )


agent_registry.register(JsonOutputAgent())
