# prepare.py
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

import os
import json
import requests
import logging
import subprocess

REPO_KEY = "https://repo.vanillaos.org/{codename}/KEY.gpg"
REPO_LIST_URL = "https://repo.vanillaos.org/{codename}/vanilla-os.list"
REPO_KEY_LOCATION = "/usr/share/keyrings/vanilla-archive-keyring.gpg"
REPO_LIST_LOCATION = "/etc/apt/sources.list.d/vanilla-os.list"

logger = logging.getLogger("VanillaUpdater::UpgradeTransactionPrepare")


class UpdatePreparer:

    def __init__(self, update: "Update"):
        self.__update = update
        
    def __download_repo_key(self):
        logger.info('Downloading repo key...')
        response = requests.get(REPO_KEY.format(codename=self.__update.codename))
        tmp = '/tmp/vanilla-archive-keyring.gpg'

        if response.status_code == 200:
            if os.path.exists(tmp):
                os.remove(tmp)

            with open(tmp, 'w') as f:
                f.write(response.text)
                return True
                
        logger.error('Failed to download repo key')
        return False

    def __download_repo_list(self):
        logger.info('Downloading repo list...')
        response = requests.get(REPO_LIST_URL.format(codename=self.__update.codename))
        tmp = '/tmp/vanilla-os.list'

        if response.status_code == 200:
            if os.path.exists(tmp):
                os.remove(tmp)

            with open(tmp, 'w') as f:
                f.write(response.text)
                return True
                
        logger.error('Failed to download repo list')
        return False

    def __install_repo_key(self):
        logger.info('Installing repo key...')
        tmp_key = '/tmp/vanilla-archive-keyring.gpg'
        
        proc = subprocess.run(['gpg', '--dearmor', tmp_key])
        if proc.returncode != 0:
            logger.error('Failed to dearmor repo key')
            return False

        proc = subprocess.run(['sudo', 'mv', tmp_key, REPO_KEY_LOCATION])
        if proc.returncode != 0:
            logger.error('Failed to move repo key')
            return False

        return True

    def __install_repo_list(self):
        logger.info('Installing repo list...')
        tmp_list = '/tmp/vanilla-os.list'

        if os.path.exists(REPO_LIST_LOCATION):
            os.rename(REPO_LIST_LOCATION, REPO_LIST_LOCATION + '.bak')

        proc = subprocess.run(['sudo', 'mv', tmp_list, REPO_LIST_LOCATION])
        if proc.returncode != 0:
            logger.error('Failed to move new repo list')
            return False

        return True

    def __update_repo(self):
        logger.info('Updating repo...')
        proc = subprocess.run(['sudo', 'apt', 'update'])
        if proc.returncode != 0:
            logger.error('Failed to update repo')
            return False

        return True

    def __download_updates(self):
        logger.info('Downloading updates...')
        proc = subprocess.run(['pkcon', 'update', '--only-download', '--noninteractive'])
        if proc.returncode != 0:
            logger.error('Failed to download updates')
            return False

        return True

    def run(self):
        logger.info('Preparing upgrade transaction...')

        if not self.__download_repo_key():
            return False

        if not self.__download_repo_list():
            return False

        if not self.__install_repo_key():
            return False

        if not self.__install_repo_list():
            return False

        if not self.__update_repo():
            return False

        if not self.__download_updates():
            return False

        logger.info('Upgrade transaction prepared')
        return True
