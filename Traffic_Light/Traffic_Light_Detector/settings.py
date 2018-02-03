import os
# noinspection PyPackageRequirements
from dotenv import load_dotenv


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GLOBAL_LOG = str2bool(os.environ.get("GLOBAL_LOG"))
LOG_PATH = os.environ.get("LOG_PATH")
CAMERAS_PATH = os.environ.get("CAMERAS_PATH")