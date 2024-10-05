# Imports
from .chord import Chord, join
from .node import Node, get_ip_port, GLOBAL_LOOPBACK_IP
from loguru import logger
import sys, os

send_data = Node.send_data

__all__ = ['Chord', 'join', 'Node', 'get_ip_port', 'GLOBAL_LOOPBACK_IP']

__author__ = "Dheekshith Mekala (Arth9r)"
__author_email__ = "dheekshithdev98@gmail.com"

# Logger
# Remove the default logger
logger.remove()

# Get the absolute path of the directory where setup.py is located
# current_directory = os.path.dirname(os.path.abspath(__file__))
# print(current_directory)

# Add handler for info logs to file.log
logger.add("libChord.log", level="INFO", filter=lambda record: record["level"].name == "INFO", enqueue=True,
           rotation="500 MB", retention="10 days", compression="zip")

# Add the default handler for other logs (outputting to stderr by default)
logger.add(sys.stderr, filter=lambda record: record["level"].name != "INFO")

logger.success("libChord successfully initialized.")
