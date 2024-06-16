import ssl
import pip

ssl._create_default_https_context = ssl._create_unverified_context
with open("requirements.txt") as requirements:
    for req in requirements:
        pip.main(["install", req])
