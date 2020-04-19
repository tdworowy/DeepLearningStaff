import subprocess
import sys

if __name__ == "__main__":
    print(sys.argv[1])
    for container_name in sys.argv[1].split("\n"):
        print(container_name)
        try:
            subprocess.Popen([f"docker logs -f {container_name} > {container_name}.log"], shell=True)
        except  Exception:
            pass