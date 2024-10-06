"""
Module Name: openia_assistant.py.

Description: Manages OpenAI assistants including creation, updating, deletion, and listing.

License: MIT.
"""
from __future__ import annotations

import enum

from openai.pagination import SyncCursorPage
from covacha_IA.openia_base import OpeniaBase
from openai.types.beta import Assistant
from openai.types.beta import AssistantDeleted


class TypeAssistantEnum(enum.Enum):
    """Enum for different types of OpenAI tools."""
    CODE_INTERPRETER = "code_interpreter"
    BROWSER = "browser"
    DALLE = "dalle"
    FILE_MANAGEMENT = "file_management"
    FILE_SEARCH = "file_search"


class OpeniaAssistant(OpeniaBase):
    """
    Manages OpenAI assistants.
    """

    def create_assistant(self, name: str, description: str, tools: list[TypeAssistantEnum]) -> Assistant:
        """
        Creates a new OpenAI assistant.
        """
        try:
            assistant = self.openIA.beta.assistants.create(
                name=name,
                description=description,
                tools=[tool.value for tool in tools],
                model=self.get_model(),
            )
            return assistant
        except Exception as e:
            print(f"Error creating assistant: {e}")
            return None

    def update_assistant(self, assistant_id: str, description: str, tools: list[TypeAssistantEnum]) -> Assistant:
        """
        Updates an existing OpenAI assistant.
        """
        try:
            assistant = self.openIA.beta.assistants.update(
                assistant_id=assistant_id,
                description=description,
                tools=[tool.value for tool in tools],
            )
            return assistant
        except Exception as e:
            print(f"Error updating assistant: {e}")
            return None

    def delete_assistant(self, assistant_id: str) -> AssistantDeleted:
        """
        Deletes an OpenAI assistant.
        """
        try:
            response = self.openIA.beta.assistants.delete(assistant_id=assistant_id)
            return response
        except Exception as e:
            print(f"Error deleting assistant: {e}")
            return None

    def list_assistants(self) -> SyncCursorPage[Assistant]:
        """
        Lists all OpenAI assistants.
        """
        try:
            response = self.openIA.beta.assistants.list()
            return response
        except Exception as e:
            print(f"Error listing assistants: {e}")
            return None
