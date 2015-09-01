import os
# import os.path
import sys
import random
import string
import yaml

system_random = random.SystemRandom()

MONGODB_USERNAME = "hackemergency"
MONGODB_NAME = "hackemergency_live"

RABBITMQ_USERNAME = "hackemergency"




def generate_random_string(length=20):
    chars = [system_random.choice(string.ascii_letters) for _ in range(length)]
    return "".join(chars)


VARS_NEEDED = {
    "RABBITMQ_USERNAME": RABBITMQ_USERNAME,
    "RABBITMQ_PASSWORD": generate_random_string,
    "MONGODB_NAME": MONGODB_NAME,
    "MONGODB_USERNAME": MONGODB_USERNAME,
    "MONGODB_PASSWORD": generate_random_string,
}

def generate_config(config_path="./persistence.yaml"):
    if os.path.isfile(config_path):
        sys.stderr.write("File {} already exists\n".format(config_path))
    else:
        _create_config(config_path)


def _create_config(config_path):
    output = {"config": {}}
    sys.stdout.write("Set the following variables in CodeShip\n")
    for var_name, source in VARS_NEEDED.items():
        if callable(source):
            output["config"][var_name] = source()
        else:
            output["config"][var_name] = source
        var_output = "{} - {}\n".format(var_name, output["config"][var_name])
        sys.stdout.write(var_output)
    with open(config_path, "w") as config_file:
        config_file.write(yaml.dump(output, default_flow_style=False))


def _delete_config(config_path):
    if os.path.isfile(config_path):
        os.remove(config_path)
    else:
        sys.stderr.write("File {} does not exist\n".format(config_path))


def regenerate_config(config_path="./persistence.yaml"):
    _delete_config(config_path)
    _create_config(config_path)
