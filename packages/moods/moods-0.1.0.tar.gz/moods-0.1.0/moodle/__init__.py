"""
Moodle API Client

Powered by `tiny-api-client`
"""

import logging
from .api import MoodleSession

__all__ = ['MoodleSession']

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
