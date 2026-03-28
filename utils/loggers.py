import logging
from typing import Any

#  TODO: Implement log saving mechanism either in log files or inside DB via redis
class Logger:

    def __init__(self, file_name: str):
        self.logger = logging.getLogger(__name__)
        self.file_name = file_name
        
    def get_log_format(self) -> str:
        return f"[{self.file_name}] - [%(asctime)s] - [%(levelname)s]  - %(message)s"
    
    def get_date_format(self) -> str:
        return "%Y-%m-%d %H:%M:%S"
    
    def log(self, message: Any):
        logging.basicConfig(format=self.get_log_format(), datefmt=self.get_date_format(), level=logging.DEBUG)
        self.logger.info(message)
        
    def debug(self, message: Any):
        logging.basicConfig(format=self.get_log_format(), datefmt=self.get_date_format(), level=logging.DEBUG)
        self.logger.debug(message)
        
    def warn(self, message: Any):
        logging.basicConfig(format=self.get_log_format(), datefmt=self.get_date_format(), level=logging.DEBUG)
        self.logger.warn(message)
        
    def error(self, message: Any):
        logging.basicConfig(format=self.get_log_format(), datefmt=self.get_date_format(), level=logging.DEBUG)
        self.logger.error(message)
