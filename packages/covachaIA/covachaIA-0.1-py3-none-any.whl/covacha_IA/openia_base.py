"""
Module Name: openia_base.py.

Description: Base repository for OpenAI operations.

License: MIT.
"""
from __future__ import annotations

from covacha_IA.config import get_env_variable
from openai import OpenAI


class OpeniaBase:
    """
    Base class for OpenAI operations.
    """

    def __init__(self):
        """
        Initializes the OpeniaBase with API credentials.
        Raises an EnvironmentError if any required environment variable is missing.
        """
        self.model = self._get_env_variable("CHATGPT_MODEL")
        self.openIA = OpenAI(
            api_key=self._get_env_variable("OPENAI_API_KEY"),
            organization=self._get_env_variable("CHATGPT_ORG"),
            project=self._get_env_variable("CHATGPT_PROJECT"),
        )

    def _get_env_variable(self, var_name: str) -> str:
        """
        Fetches the environment variable and raises an exception if it's not found.
        """
        value = get_env_variable(var_name)
        if not value:
            raise EnvironmentError(f"La variable de entorno {var_name} no está definida en .env")
        return value

    def get_model(self) -> str:
        """
        Returns the model name.
        """
        return self.model

    def get_openIA(self) -> OpenAI:
        """
        Returns the OpenAI client instance.
        """
        return self.openIA
