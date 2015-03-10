# Copyright (C) 2006-2014 VisoTech Softwareentwicklungsges.m.b.H.
#
# This file is part of ENTE, an in-memory graph database.
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

# NeuroBase instances created too early during the startup process
# embed a null Ente pointer and thus not work properly. This module
# contains the only bound NeuroBase method for which this matters.

import visotech
nb = visotech.neurobase.NeuroBase.instance
if nb.is_vtappd():
    get_subnode_val = nb.get_subnode_val
