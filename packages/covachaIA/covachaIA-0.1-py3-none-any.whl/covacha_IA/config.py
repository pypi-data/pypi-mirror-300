import os
from dotenv import load_dotenv

load_dotenv()

# Función para obtener variables de entorno y lanzar un error si no existen
def get_env_variable(var_name):
    """Obtiene la variable de entorno o lanza un error."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"La variable de entorno {var_name} no está definida en .env"
        raise EnvironmentError(error_msg)

OPENAI_API_KEY = get_env_variable('OPENAI_API_KEY')