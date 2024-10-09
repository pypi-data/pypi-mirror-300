# stdlib
import os

__DIR_CURRENT = os.path.dirname(__file__)
DIR_CONFIGS = os.path.join(__DIR_CURRENT, "configs")
__basenames = os.listdir(DIR_CONFIGS)
PARSER_CONFIGS = [os.path.join(DIR_CONFIGS, f) for f in __basenames]
PARSER_CONFIGS.sort()
