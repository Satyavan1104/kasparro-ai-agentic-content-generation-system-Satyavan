"""
Core Agent Framework

Defines the base agent interface and common utilities for the agentic system.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentMessage:
    """Message passed between agents"""

    sender: str
    receiver: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: Optional[str] = None


@dataclass
class AgentResult:
    """Standardized agent output"""

    agent_name: str
    status: AgentStatus
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    
    Each agent must:
    - Have a single responsibility
    - Define clear input/output contracts
    - Maintain no hidden global state
    """
    
    def __init__(self, name: str):
        self.name = name
        self.status = AgentStatus.IDLE
        self.input_schema = None
        self.output_schema = None
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Process input data and return standardized result.
        
        Args:
            input_data: Dictionary containing agent input
            
        Returns:
            AgentResult with processed data or errors
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate that input data meets agent requirements.
        
        Args:
            input_data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities and metadata"""
        return {
            "name": self.name,
            "status": self.status.value,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema
        }


class AgentRegistry:
    """Registry for managing available agents"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
    
    def register(self, agent: BaseAgent) -> None:
        """Register an agent"""
        self._agents[agent.name] = agent
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name"""
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self._agents.keys())
    
    def get_all_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get capabilities of all registered agents"""
        return {name: agent.get_capabilities() for name, agent in self._agents.items()}


# Global agent registry instance
agent_registry = AgentRegistry()
