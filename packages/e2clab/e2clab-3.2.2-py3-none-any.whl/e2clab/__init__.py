# flake8: noqa
# Loading env variables before anything
ENV_FILE = ".e2c_env"
from dotenv import load_dotenv

loaded_dotenv = load_dotenv(ENV_FILE)
from e2clab.optimizer import Optimizer
from e2clab.services import Service
