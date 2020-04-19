import subprocess
import sys

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        subprocess.Popen([f"docker logs -f {arg} > {arg.replace('/','_')}.log"])
