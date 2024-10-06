"""
Module Name: open_ia.py.

Description: Base repository for DynamoDB operations with pagination and sorting.

License: MIT.
"""
import threading
from openai import OpenAI


class OpenIa:
    """
    Clase que maneja interacciones con OpenAI y permite la ejecución en múltiples threads
    """

    def __init__(self, model: str, api_key: str, org: str, project: str):
        """
        Inicializa OpenAI con los parámetros proporcionados
        """
        self.model = model
        self.messages = []
        self.openIA = OpenAI(api_key=api_key, organization=org, project=project)

    def user_question(self, question: str):
        """
        Función que simula el comportamiento del usuario y añade la pregunta
        """
        self.messages.append({"role": 'user', "content": question})

        try:
            response = self.openIA.chat.completions.create(
                model=self.model,
                messages=self.messages,
            )
            self._handle_stream(response)
        except Exception as e:
            print(f"Error during user question: {e}")

    def _handle_stream(self, stream):
        """
        Función que maneja el stream de respuestas
        """
        try:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
        except Exception as e:
            print(f"Error handling stream: {e}")
