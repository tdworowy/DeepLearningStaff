import sys
import yaml
if __name__ == "__main__":
    fname = "config.yaml"

    ip = sys.argv[1]

    stream = open(fname, 'r')

    data = yaml.load(stream)
    data["mongo_host"] = ip
    data["nats_host"] = ip

    with open(fname, 'w') as yaml_file:
        yaml_file.write(yaml.dump(data, default_flow_style=False))