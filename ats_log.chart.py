# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: JackGlobetrotter (JackGlobetrotter)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
from bases.FrameworkServices.LogService import LogService

priority = 90000

ORDER = [
    'CPU', 'CPUTemp','HDD', 'HDDTemp'
]

CHARTS = {
    'CPU': {
        'options': [None, 'CPU Fan Speed', 'speed', 'CPU', 'CPU', 'line'],
        'lines': [
            ['fan_cpu', 'fan speed']
        ]
    },
    'CPUTemp': {
        'options': [None, 'CPU Temperature', 'Celsius', 'CPU', 'CPU', 'line'],
        'lines': [
            ['cpu', 'cpu temperature']
        ]
    },
    'HDD': {
        'options': [None, 'HDD Fan Speed', 'speed', 'HDD','HDD',  'line'],
        'lines': [
            ['fan_hdd', 'fan speed']
        ]
    },
    'HDDTemp': {
        'options': [None, 'HDD Temperature', 'Celsius', 'HDD','HDD',  'line'],
        'lines': [
            ['hdd', 'hdd temperature']
        ]
    }    
}

class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.log_path = self.configuration.get('log_path')

    def check(self):
        """
        :return: bool
        """

        if not os.access(self.log_path, os.R_OK):
            self.error('{0} is not readable'.format(self.log_path))
            return False

        if os.path.getsize(self.log_path) == 0:
            self.error('{0} is empty'.format(self.log_path))
            return False
        return True

    def _get_raw_data(self):
        """
        Open log file
        :return: str
        """

        try:
            with open(self.log_path) as log:
                log.seek(os.path.getsize(self.log_path)-80)
                raw_data = log.readlines() or None
        except OSError:
            return None
        else:
            return raw_data

    def get_data(self):
        raw_data = self._get_raw_data()
        if not raw_data:
            return None
        
        for row in raw_data:
            pass

        if(len(row)>3):
            try:
                reg = re.compile("\d+(?=°c)|(?<=set to )[0-9]+\d+(?:°c)|(?<=set to )[0-9]+", re.IGNORECASE);
                d = reg.findall(row)
                return {
                    'cpu':int(d[0]),
                    "hdd":int(d[2]),
                    "fan_cpu":int(d[1]),
                    "fan_hdd":int(d[3])
                }
            except:
                return None