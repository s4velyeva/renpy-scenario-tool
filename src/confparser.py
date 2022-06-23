from xml.dom.minidom import Attr
import toml
import os

from rst_logging import LogLevel, Logger


logger = Logger('/tmp/renpy-scenario-tool.log')

class ConfParser():
    def __init__(self, config_paths):
        for i in config_paths:
            if not os.path.exists(i):
                logger(f'File {i} doesn\'t exist', 'initialization', LogLevel.WARN)
            else:
                self.config = i

        try:
            self.config_toml = self.__parse(self.config)
        except AttributeError:
            logger(f'Failed to initialize config, file doesn\'t exist', 'initialization', LogLevel.ERROR)
            exit(1)

    def __parse(self, config):
        return toml.load(config)