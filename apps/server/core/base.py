from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    name: str
    def __init__(self, name: str):
        self.name = name
    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
    def register(self, agent: BaseAgent):
        self._agents[agent.name] = agent
    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not registered")
        return self._agents[name]

registry = AgentRegistry()
