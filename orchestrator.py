"""
Orchestrator

Defines the automation graph (pipeline) and executes agents in sequence.
No hidden global state: all state is passed via explicit inputs/outputs between agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from agent_framework import AgentResult, AgentStatus, agent_registry

# Import agents so they self-register with the registry
import competitor_agent  # noqa: F401
import content_generator_agent  # noqa: F401
import data_parser_agent  # noqa: F401
import json_output_agent  # noqa: F401
import question_generator_agent  # noqa: F401


@dataclass(frozen=True)
class PipelineStep:
    step_name: str
    agent_name: str


class ContentOrchestrator:
    """Runs the agentic pipeline and returns outputs + artifacts."""

    def __init__(self):
        self.steps: List[PipelineStep] = [
            PipelineStep(step_name="parse_product", agent_name="DataParserAgent"),
            PipelineStep(step_name="generate_questions", agent_name="QuestionGeneratorAgent"),
            PipelineStep(step_name="generate_competitor", agent_name="CompetitorAgent"),
            PipelineStep(step_name="generate_pages", agent_name="ContentGeneratorAgent"),
            PipelineStep(step_name="write_json", agent_name="JsonOutputAgent"),
        ]

    def get_graph(self) -> Dict[str, Any]:
        """Return a machine-readable representation of the automation graph."""

        nodes = [
            {
                "id": step.step_name,
                "type": "agent_step",
                "agent": step.agent_name,
            }
            for step in self.steps
        ]

        edges = []
        for i in range(1, len(self.steps)):
            edges.append(
                {
                    "from": self.steps[i - 1].step_name,
                    "to": self.steps[i].step_name,
                }
            )

        return {
            "graph_type": "pipeline",
            "entry": self.steps[0].step_name if self.steps else None,
            "exit": self.steps[-1].step_name if self.steps else None,
            "nodes": nodes,
            "edges": edges,
        }

    def run_pipeline(self, raw_product_data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Run the full pipeline and return artifacts (including final pages + file paths)."""

        artifacts: Dict[str, Any] = {
            "raw_input": raw_product_data,
            "steps": [],
        }

        artifacts["graph"] = self.get_graph()

        parsed = self._run_agent("DataParserAgent", raw_product_data)
        artifacts["parsed_product"] = parsed

        questions = self._run_agent("QuestionGeneratorAgent", parsed)
        artifacts["questions"] = questions

        competitor_out = self._run_agent("CompetitorAgent", parsed)
        product_b = competitor_out["product_b"]
        artifacts["product_b"] = product_b

        pages_input = {
            "product_a": parsed,
            "product_b": product_b,
            "questions": questions,
        }
        pages = self._run_agent("ContentGeneratorAgent", pages_input)
        artifacts["pages"] = pages

        write_input = {
            "output_dir": output_dir,
            "pages": pages,
            "graph": artifacts["graph"],
        }
        written = self._run_agent("JsonOutputAgent", write_input)
        artifacts["written_files"] = written

        return artifacts

    def _run_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        agent = agent_registry.get_agent(agent_name)
        if agent is None:
            raise ValueError(f"Agent not registered: {agent_name}")

        result: AgentResult = agent.process(input_data)
        if result.status != AgentStatus.COMPLETED or result.data is None:
            errors = result.errors or ["Unknown error"]
            raise RuntimeError(f"Agent {agent_name} failed: {errors}")

        return result.data
