import yaml
from rich.console import Console
from rich.logging import RichHandler
from pathlib import Path
from random import randrange, seed
import logging
import os
import toml
from box import Box

# -----------------------------------------------------------------

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")
console = Console()

# -----------------------------------------------------------------


def print(*args, **kwargs):
    console.print(*args, **kwargs)


# -----------------------------------------------------------------


def color_value(value: str):
    seed(value.lower())
    r, g, b = [str(hex(randrange(25, 255))[2:]) for _ in range(3)]
    value_colored = f"[bold #{r}{g}{b}]{value}[/]"

    return value_colored


# -----------------------------------------------------------------

CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
CONFIG_FILE = CONFIG_HOME / "novara" / "config.yml"
SSHKEY_FILE = CONFIG_HOME / "novara" / "novara.key"
SOCKET_FILE = CONFIG_HOME / "novara" / "novara_docker.sock"

def write_config(config: dict):
    try:
        dot_config = CONFIG_HOME
        if not dot_config.exists():
            logger.info(f"creating directory {dot_config}")
            dot_config.mkdir()
        config_directory = CONFIG_FILE.parent
        if not config_directory.exists():
            logger.info(f"creating directory {config_directory}")
            config_directory.mkdir()
        yaml.dump(config, open(CONFIG_FILE, "w"))
    except OSError:
        logger.error("Couldn't create the config file it's not writable")
        exit()
    # --------------
    try:
        with open(SSHKEY_FILE, "w") as f:
            f.write(config["ssh_privatekey"])
    except OSError:
        logger.error("Couldn't create the SSH-key it's not writable")
        exit()
    # --------------
    try:
        os.chmod(SSHKEY_FILE, 0o600)
    except OSError:
        logger.error("Couldn't change the SSH-key's permissions")
        exit()
    # --------------
    logger.info("Testing SSH connection...")

    process = os.popen(f"ssh -o StrictHostKeyChecking=accept-new -i {SSHKEY_FILE} -p {config['ssh_port']} {config['ssh_user']}@{config['ssh_url']} 'echo :3'")
    output = process.read()
    exit_code = process.close()
    exit_code = 0 if exit_code == None else exit_code

    if exit_code != 0:
        logger.error("Failed to establish SSH connection!!!")
        logger.debug(f"Is the public key on the target's authorized_keys file?")
        logger.error(output)
        exit()
    logger.info("ssh connections succesfull")

def get_current_config():
    try:
        with open("novara.toml", "r") as f:
            # exploit_config = toml.load(f)
            toml_parsed = toml.load(f)
    except (OSError, FileNotFoundError):
        return None
    return Box(toml_parsed)