import importlib.util
import os
import sys
from subprocess import run

from ..node.wsnode import WSNode

HTTPSERVER = "httpserver"
REGISTRY = "registry"


def run_agentic(*, mode: str, port: int, dev: bool, registry: str) -> None:
    if not os.path.isfile("pyproject.toml"):
        print("!!!!")
        print("ERROR:You have to run this command in the root folder of your project")
        print("!!!!")
        sys.exit(1)
    if mode == HTTPSERVER:
        cmd = ["fastapi"]
        cmd += ["dev", "--reload"] if dev else ["run"]
        cmd += ["--port", str(port)]
        cmd += ["src/agentic/agentic_node.py"]
        print("Running command: ", cmd)
        run(cmd, check=True)
    elif mode == REGISTRY:
        # import workflows from the config file
        config_path = os.path.join(os.getcwd(), "src/agentic/agentic_config.py")
        spec = importlib.util.spec_from_file_location("agentic_config", config_path)
        if spec is None:
            raise ValueError("Invalid config file")
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ValueError("Invalid config file")
        sys.path.append(os.getcwd()+"/src")
        spec.loader.exec_module(module)
        WSNode(config=module.config, registry= registry).connect_to_registry()

    else:
        raise ValueError("Invalid mode")
