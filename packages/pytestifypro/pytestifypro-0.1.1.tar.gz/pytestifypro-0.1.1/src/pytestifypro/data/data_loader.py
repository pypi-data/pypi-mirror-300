import yaml
import os

# def load_config(file_path='src/pytestifypro/config/config.yaml'):
#     """
#     Load configuration parameters from a YAML file.
#     """
#     with open(file_path, 'r') as file:
#         config = yaml.safe_load(file)
#     return config

def load_config():
    print("Loading config...")  # Debug statement to see if this is called
    env = os.getenv("TEST_ENV", "dev")  # Default to 'dev' if no env is specified
    print(f"Environment: {env}")  # See what environment is being used
    with open("src/pytestifypro/config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    print(f"Config before environment merge: {config}")  # Debug output to see the base config
    environment_config = config.get("environments", {}).get(env, {})
    print(f"Environment-specific config: {environment_config}")  # Debug to see environment-specific config

    # Merge environment-specific config with the base config
    merged_config = {**config, **environment_config}

    print(f"Final merged config: {merged_config}")  # Debug to see final merged config
    return merged_config


def load_schema(file_path='src/pytestifypro/config/schema_config.yaml'):
    """
    Load schema parameters from a YAML file.
    """
    with open(file_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema


# def load_data(file_path):
#     """Load test data from a file."""
#     with open(file_path, 'r') as file:
#         data = file.read()
#     return data

