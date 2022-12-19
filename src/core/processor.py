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

REPO_SOURCES = """deb http://ppa.launchpad.net/vanilla-os/testing/ubuntu {codename} main
# deb-src http://ppa.launchpad.net/vanilla-os/testing/ubuntu {codename} main"""
REPO_LIST_LOCATION = "/tmp/overlayfs-combiner/etc/apt/sources.list.d/vanilla.list"

logger = logging.getLogger("VanillaUpdater::UpgradeTransactionPrepare")


class UpdateProcessor:

    def __init__(self, update: "Update"):
        self.__update = update

    def __check_transactions_lock(self):
        return os.path.exists("/tmp/abroot-transactions.lock")

    def run(self):
        if self.__check_transactions_lock():
            logger.error("Another transaction is running or a reboot is required.")
            return False

        logger.info('Launching upgrade transaction...')

        logger.info('Starting abroot shell...')
        abroot = subprocess.Popen(['abroot', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        logger.info('Replacing vanilla.list...')
        with open(REPO_LIST_LOCATION, 'w') as f:
            f.write(REPO_SOURCES.format(codename=self.__update.codename))

        logger.info('Updating sources...')
        abroot.stdin.write(b'apt update\n')

        logger.info('Upgrading packages...')
        abroot.stdin.write(b'apt upgrade\n')

        logger.info('Upgrading distro...')
        abroot.stdin.write(b'apt dist-upgrade\n')

        logger.info('Exiting abroot shell...')
        abroot.stdin.write(b'exit\n')

        logger.info('Waiting for abroot shell to exit...')
        abroot.wait()

        if abroot.returncode != 0:
            logger.error('Abroot shell exited with error code {}'.format(abroot.returncode))
            return False

        logger.info('Upgrade transaction terminated.')
        return True
