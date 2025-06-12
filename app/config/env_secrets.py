import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Set the {var_name} environment variable")
    return value