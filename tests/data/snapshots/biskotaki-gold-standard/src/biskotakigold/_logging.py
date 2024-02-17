"""Set up Application Logs

This module defines how the emitted application logs are handled and where
they are written/streamed.
The application logs are written in full details (ie with timestamps) to a file
and also streamed to the console in a more concise format.

# Console/Terminal Log:
    - We Stream Logs of INFO (and above) Level on Console's stderr
    - The rendered Log format is: <logger name>: <log level> <log message>

# Disk File Log:
    - we Write Logs of ALL Levels on a Disk File
    - The rendered Log format is: <timestamp> <logger name>: <log level> <log message>
    - The FILE_TARGET_LOGS, variable (see below), defines the path to the log file

Log Levels:
- CRITICAL
- ERROR
- WARNING
- INFO
- DEBUG

Usage:
    Do a 'from . import _logging' in the root __init__.py of your package and
    all submodules 'inherit' the logging configuration
"""

import logging

# for 'biskotaki' app/code
FILE_TARGET_LOGS = 'biskotaki.log'

#### FILE LOGGING
# set up logging to file for DEBUG Level and above
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename=FILE_TARGET_LOGS,
    filemode='w',
)

#### CONSOLE LOGGING
console = logging.StreamHandler()

### Handler which writes DEBUG messages or higher to the sys.stderr ###
console.setLevel(logging.DEBUG)
# console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


# Now, we can log to the root logger, or any other logger. First the root...
# logging.info('Blah blah')

# Now, define a couple of other loggers which might represent areas in your
# application:

# logger1 = logging.getLogger('myapp.area1')
# logger2 = logging.getLogger('myapp.area2')
# logger3 = logging.getLogger(__name__)

# logger1.debug('balh blah')
# logger1.info('balh blah')
# logger2.warning('balh blah')
# logger3.error('balh blah')
