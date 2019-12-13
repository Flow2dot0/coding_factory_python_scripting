import yaml


def load_config(config_file):
    """Loading the yaml config file
    :args: yaml file
    :return: stream
    """
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
