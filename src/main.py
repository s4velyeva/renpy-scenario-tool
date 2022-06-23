#!.pyenv/bin/python

import rst_logging
import confparser

from pathlib import Path

CONFIG_PATHS = [f'{Path.home()}/.config/renpy-st/config', 'config', '/usr/share/renpy-st/config']

logger = rst_logging.Logger('/tmp/renpy-scenario-tool.log')
confer = confparser.ConfParser(CONFIG_PATHS)

logger.set_task('configure')

try:
    if confer.config_toml['Options']['debug']:
        logger('Debug mode activated')

except KeyError:
    logger(f'Main \'Options\' section doesn\'t exist', 'configure', rst_logging.LogLevel.ERROR)
    exit(1)


from odf import text, teletype
from odf.opendocument import load
import sys

def find_key(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key(v, value)
            if p:
                return [k] + p
        elif v == value:
            return [k]

textdoc = load(sys.argv[1])
allparagraphs = textdoc.getElementsByType(text.P)

logger.set_task('parsing')

print('  ---------------------------------------------------------------------------------')

count = 1

output = open('output.rpy', 'w')

for lc in allparagraphs:
    line = teletype.extractText(lc)

    if (confer.config_toml['Options']['verbose']):
        print(f'{count} | {line}')

    for i in confer.config_toml['Characters']:
        character = confer.config_toml["Characters"][i]
        if line.startswith(character + ': '):
            output.write(f'{find_key(confer.config_toml, character)[1]} \"{line.replace(character + ": ", "")}\"\n')

        if not line.startswith(character + ': ') and not line.startswith('$'):
            output.write(f'\"{line}\"\n')

    if line.strip().startswith('$'):
        output.write(f'{line}\n')

    count += 1