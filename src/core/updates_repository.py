# updates_repository.py
#
# Copyright 2022 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import requests
import logging

UPDATES_URL = 'https://raw.githubusercontent.com/Vanilla-OS/info/main/updates.json'

logger = logging.getLogger("VanillaUpdater::UpdatesRepository")


class Update:
    
    def __init__(self, version, codename):
        self.version = version
        self.codename = codename

    def __str__(self):
        return f'Version: {self.version}, Codename: {self.codename}'

    def __repr__(self):
        return self.__str__()


class UpdatesRepository:

    def __init__(self):
        self.__updates = self.__get_updates()

    def __get_updates(self):
        logger.info('Getting updates...')

        updates = []
        response = requests.get(UPDATES_URL)

        if response.status_code == 200:
            data = json.loads(response.text)
            for version in data:
                updates.append(Update(version, data[version]['codename']))
        
        logger.info('Updates: %s', updates)

        return updates
    
    def get_next_update(self, version):
        logger.info('Getting next update for version %s', version)

        for update in self.__updates:
            if update.version > version:
                logger.info('Next update: %s', update)
                return update
        
        logger.info('No updates found')

        return None

    @property
    def all_updates(self):
        return self.__updates

    @property
    def latest_update(self):
        return self.__updates[-1]
