__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2021.11.29"

import csv
import json
import os

from dateutil import tz

from datetime import datetime, timedelta
from pytz import timezone
import pytz


class Tz(object):
    """
    TODO: Implement class
    """

    @classmethod
    def common_timezone_list(cls):
        # return a list of strings with values like this: US/Central
        return pytz.common_timezones

    @classmethod
    def gmt_tz(cls):
        return timezone('GMT')

    @classmethod
    def paris_tz(cls):
        return timezone('Europe/Paris')

    @classmethod
    def uk_tz(cls):
        return timezone('Europe/London')

    @classmethod
    def eastus_tz(cls):
        return timezone('America/New_York')

    @classmethod
    def westus_tz(cls):
        return timezone('America/Los_Angeles')

    @classmethod
    def explore(cls):
        utc = pytz.utc
        print(utc)
        print(utc.zone)

        eastern = timezone('US/Eastern')
        print(eastern.zone)

        amsterdam = timezone('Europe/Amsterdam')
        print(amsterdam.zone)

        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
