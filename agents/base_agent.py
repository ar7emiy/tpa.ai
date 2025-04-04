# agents/base_agent.py
import os
from typing import Dict, List, Optional, Tuple, Any
import datetime
import uuid
import json
from google.generativeai import GenerativeModel
from google.generativeai.types import FunctionDeclaration, Tool, GenerateContentConfig

configure(api_key=SETTINGS["GOOGLE_API_KEY"])

class BaseAgent:
    def __init__(self, model_name: str = "gemini-2.0-pro"):
        """Initialize a base agent."""
        self.model_name = model_name
        self.agent_name = self.__class__.__name__
    
    def _format_system_prompt(self, role: str, instructions: str) -> str:
        """Format the system prompt with the agent's role and instructions."""
        return f"""You are the {role} in a workers' compensation claims processing system.
        
{instructions}

Current timestamp: {datetime.datetime.now().isoformat()}
"""
    
    def create_gemini_model(self, system_instruction: str, tools: List[Tool] = None):
        """Create a Gemini model with the given system instruction and tools."""
        return GenerativeModel(
            model_name=self.model_name,
            generation_config=GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools,
            )
        )
    
    def handle_function_call(self, function_name: str, function_args: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Handle a function call from the model.
        
        Args:
            function_name: The name of the function called
            function_args: The arguments to the function
            state: The current state
            
        Returns:
            response: The response to send back to the model
            updated_state: Any updates to the state
        """
        raise NotImplementedError("Subclasses must implement handle_function_call")
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return the updated state.
        
        Args:
            state: The current state
            
        Returns:
            updated_state: The updated state
        """
        raise NotImplementedError("Subclasses must implement process")
    
    def reset(self):
        """Reset the agent's state."""
        pass
