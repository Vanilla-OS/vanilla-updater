# window.py
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

from gi.repository import Adw
from gi.repository import Gtk

from .core.distro import Distro
from .core.updates_repository import UpdatesRepository

from .utils.run_async import RunAsync


@Gtk.Template(resource_path='/org/vanillaos/VanillaUpdater/window.ui')
class VanillaUpdaterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VanillaUpdaterWindow'

    stack_main = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__loader()

    def __loader(self):
        def async_fn():
            return Distro(), UpdatesRepository()
        
        def callback(result, *args):
            distro, updates_repo = result
            update = updates_repo.get_next_update(distro.version)
            
            if update:
                self.stack_main.set_visible_child_name('found')
            else:
                self.stack_main.set_visible_child_name('updated')

        RunAsync(async_fn, callback)


        