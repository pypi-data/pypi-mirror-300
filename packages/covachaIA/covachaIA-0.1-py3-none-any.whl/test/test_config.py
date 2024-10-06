import os
from covacha_IA.config import get_env_variable
import pytest
from dotenv import load_dotenv

# Cargar el archivo .env antes de las pruebas
load_dotenv()


def test_enviroments_exists():
    """Prueba para asegurarse de que la clave de API de OpenAI está disponible."""
    assert 'OPENAI_API_KEY' in os.environ, "OPENAI_API_KEY no está definida"
    assert 'CHATGPT_ORG' in os.environ, "CHATGPT_ORG no está definida"
    assert 'CHATGPT_MODEL' in os.environ, "CHATGPT_MODEL no está definida"
    assert 'CHATGPT_PROJECT' in os.environ, "CHATGPT_PROJECT no está definida"
    assert 'CHATGPT_KEY_SERVICE' in os.environ, "CHATGPT_KEY_SERVICE no está definida"

def test_openai_api_key_is_valid():
    """Prueba de que la clave de API tiene el formato correcto (dummy test)."""
    api_key = os.getenv('OPENAI_API_KEY')
    assert api_key.startswith('sk-'), "La clave de API no parece válida"

def test_chatgpt_org_key_is_valid():
    """Prueba de que la clave de API tiene el formato correcto (dummy test)."""
    api_key = os.getenv('CHATGPT_ORG')
    assert api_key.startswith('org-'), "La clave de CHATGPT_ORG no parece válida"

def test_chatgpt_model_key_is_valid():
    """Prueba de que la clave de API tiene el formato correcto (dummy test)."""
    api_key = os.getenv('CHATGPT_MODEL')
    assert api_key.startswith('gpt-'), "La clave de CHATGPT_MODEL no parece válida"

def test_chatgpt_project_key_is_valid():
    """Prueba de que la clave de API tiene el formato correcto (dummy test)."""
    api_key = os.getenv('CHATGPT_PROJECT')
    assert api_key.startswith('proj_'), "La clave de CHATGPT_PROJECT no parece válida"

def test_chatgpt_key_service_is_valid():
    """Prueba de que la clave de API tiene el formato correcto (dummy test)."""
    api_key = os.getenv('CHATGPT_KEY_SERVICE')
    assert api_key.startswith('sk-'), "La clave de CHATGPT_KEY_SERVICE no parece válida"