import subprocess
import sys

if __name__ == "__main__":
    for container_name in sys.argv[1].split(","):
        subprocess.Popen(
            [f"docker logs -f {container_name} > {container_name}.log"], shell=True
        )
