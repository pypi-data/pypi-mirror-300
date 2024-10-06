"""
Module Name: openia_thread.py.

Description: Manages OpenAI threads including creation, updating, deletion, and running instructions.

License: MIT.
"""
from __future__ import annotations

from covacha_IA.openia_base import OpeniaBase


class OpeniaThread(OpeniaBase):
    """
    Manages OpenAI threads.
    """

    def create_thread(self):
        """
        Creates a new OpenAI thread.
        """
        try:
            response = self.openIA.beta.threads.create()
            return response
        except Exception as e:
            print(f"Error creating thread: {e}")
            return None

    def update_thread(self, thread_id: str, metadata: str):
        """
        Updates an existing OpenAI thread.
        """
        try:
            response = self.openIA.beta.threads.update(thread_id=thread_id, metadata=metadata)
            return response
        except Exception as e:
            print(f"Error updating thread: {e}")
            return None

    def delete_thread(self, thread_id: str):
        """
        Deletes an OpenAI thread.
        """
        try:
            response = self.openIA.beta.threads.delete(thread_id=thread_id)
            return response
        except Exception as e:
            print(f"Error deleting thread: {e}")
            return None

    def run_instruction(self, thread_id: str, assistant_id: str, instruction: str):
        """
        Runs an instruction on an OpenAI thread.
        """
        try:
            response = self.openIA.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instruction=instruction,
            )
            return response
        except Exception as e:
            print(f"Error running instruction: {e}")
            return None

    def add_message(self, thread_id: str, role: str, content: str):
        """
        Adds a message to an OpenAI thread.
        Role: 'system', 'user', 'assistant'.
        """
        try:
            response = self.openIA.beta.threads.messages.create(
                thread_id=thread_id,
                role=role,
                content=content,
            )
            return response
        except Exception as e:
            print(f"Error adding message: {e}")
            return None
