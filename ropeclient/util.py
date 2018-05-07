import logging
import sys

import ropeclient as rc

logger = logging.getLogger('worksclient')


def _console_log_level():
    if rc.log in ['debug', 'info']:
        return rc.log
    else:
        return None