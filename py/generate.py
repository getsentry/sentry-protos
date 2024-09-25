import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

from os import path

here = path.abspath(path.dirname(__file__))
root_dir = path.abspath(os.path.join(path.dirname(__file__), ".."))

unstable_package_pattern = re.compile(r"v\d+(?:alpha|beta|dev)")

def is_unstable(proto: str) -> bool:
    matches = unstable_package_pattern.search(proto)
    return matches != None


def build_protos():
    build_unstable = int(os.getenv("SENTRY_PROTOS_BUILD_UNSTABLE", "0"))
    if build_unstable:
        print("Including unstable protos")

    protos = glob.glob(f"{root_dir}/proto/sentry_protos/**/*.proto", recursive=True)
    with tempfile.TemporaryDirectory() as tmpd:
        for proto in protos:
            if build_unstable == 0 and is_unstable(proto):
                print(f"Skipping {proto} it is an unstable protocol")
                continue

            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "grpc_tools.protoc",
                    f"-I{root_dir}/proto",
                    f"--python_out={tmpd}",
                    f"--mypy_out={tmpd}",
                    f"--grpc_python_out={tmpd}",
                    f"--mypy_grpc_out={tmpd}",
                    proto,
                ]
            )

            if result.returncode != 0:
                sys.exit(1)

        for dir, _, files in os.walk(os.path.join(tmpd, "sentry_protos")):
            if "__init__.py" in files:
                continue
            with open(f"{dir}/__init__.py", "w") as f:
                f.write("")

        with open(f"{root_dir}/VERSION", "r") as f:
            version = f.read().strip()

        for p in os.listdir(tmpd):
            p = f"{tmpd}/{p}"
            if not os.path.isdir(p):
                continue
            with open(f"{p}/py.typed", "w") as f:
                f.write("")
            with open(f"{p}/__init__.py", "w") as f:
                f.write(f'__version__ = "{version}"\n')

        shutil.rmtree(f"{root_dir}/py/sentry_protos", ignore_errors=True)
        shutil.move(f"{tmpd}/sentry_protos", f"{root_dir}/py/sentry_protos")


if __name__ == "__main__":
    build_protos()
