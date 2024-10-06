import pytest
from covacha_IA.config import get_env_variable
from openai import OpenAI
from openia_base import OpeniaBase


class TestOpeniaBase:

    @pytest.fixture
    def mock_env_variables(self, mocker):
        # Mockear todas las variables de entorno necesarias
        mock_get_env_variable = mocker.patch('covacha_IA.config.get_env_variable')
        mock_get_env_variable.side_effect = lambda var_name: {
            "CHATGPT_MODEL": "gpt-3.5-turbo",
            "OPENAI_API_KEY": "valid_api_key",
            "CHATGPT_ORG": "valid_org",
            "CHATGPT_PROJECT": "valid_project"
        }.get(var_name)
        return mock_get_env_variable

    def test_initializes_with_valid_api_credentials(self, mock_env_variables):
        """
        Verifica que la clase se inicialice correctamente con las credenciales válidas.
        """
        openia_base = OpeniaBase()

        assert openia_base.get_model() == "gpt-3.5-turbo"
        assert openia_base.get_openIA().api_key == "valid_api_key"
        assert openia_base.get_openIA().organization == "valid_org"
        assert openia_base.get_openIA().project == "valid_project"

    @pytest.mark.parametrize("missing_var, error_message", [
        ("CHATGPT_MODEL", "La variable de entorno CHATGPT_MODEL no está definida en .env"),
        ("OPENAI_API_KEY", "La variable de entorno OPENAI_API_KEY no está definida en .env"),
        ("CHATGPT_ORG", "La variable de entorno CHATGPT_ORG no está definida en .env"),
        ("CHATGPT_PROJECT", "La variable de entorno CHATGPT_PROJECT no está definida en .env"),
    ])
    def test_missing_env_variables(self, mocker, missing_var, error_message):
        """
        Verifica que se levante un EnvironmentError si falta alguna variable de entorno.
        """
        mock_get_env_variable = mocker.patch('covacha_IA.config.get_env_variable')
        mock_get_env_variable.side_effect = lambda var_name: {
            "CHATGPT_MODEL": "gpt-3.5-turbo" if var_name != "CHATGPT_MODEL" else None,
            "OPENAI_API_KEY": "valid_api_key" if var_name != "OPENAI_API_KEY" else None,
            "CHATGPT_ORG": "valid_org" if var_name != "CHATGPT_ORG" else None,
            "CHATGPT_PROJECT": "valid_project" if var_name != "CHATGPT_PROJECT" else None
        }.get(var_name)

        with pytest.raises(EnvironmentError) as excinfo:
            OpeniaBase()

        assert str(excinfo.value) == error_message
