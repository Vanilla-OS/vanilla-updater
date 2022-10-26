# distro.py
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
import logging


logger = logging.getLogger("VanillaUpdater::Distro")


class Distro:

    def __init__(self):
        self.__id = None
        self.__id_like = None
        self.__name = None
        self.__pretty_name = None
        self.__version = None
        self.__version_id = None
        self.__version_codename = None

        self.__parse_os_release()

    def __parse_os_release(self):
        os_release = open('/etc/os-release', 'r')

        for line in os_release:
            if line.startswith('ID='):
                self.__id = line[3:].strip().replace('"', '')
            elif line.startswith('ID_LIKE='):
                self.__id_like = line[8:].strip().replace('"', '')
            elif line.startswith('NAME='):
                self.__name = line[5:].strip().replace('"', '')
            elif line.startswith('PRETTY_NAME='):
                self.__pretty_name = line[12:].strip().replace('"', '')
            elif line.startswith('VERSION='):
                self.__version = line[8:].strip().replace('"', '')
            elif line.startswith('VERSION_ID='):
                self.__version_id = line[11:].strip().replace('"', '')
            elif line.startswith('VERSION_CODENAME='):
                self.__version_codename = line[17:].strip().replace('"', '')

        os_release.close()
    
    @property
    def dict(self):
        return {
            'id': self.__id,
            'id_like': self.__id_like,
            'name': self.__name,
            'pretty_name': self.__pretty_name,
            'version': self.__version,
            'version_id': self.__version_id,
            'version_codename': self.__version_codename
        }

    @property
    def id(self):
        return self.__id

    @property
    def id_like(self):
        return self.__id_like

    @property
    def name(self):
        return self.__name

    @property
    def pretty_name(self):
        return self.__pretty_name

    @property
    def version(self):
        return self.__version

    @property
    def version_id(self):
        return self.__version_id

    @property
    def version_codename(self):
        return self.__version_codename
        
    @property
    def is_lts(self):
        return "lts" in self.__version.lower().split(" ")
