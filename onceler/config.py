import toml


# read config file

CONFIG_FILE = "onceler.toml"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return toml.load(f)


def write_config(config):
    with open(CONFIG_FILE, "w") as f:
        toml.dump(config, f)