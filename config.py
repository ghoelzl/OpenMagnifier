# Copyright 2011-2013 Guenther Hoelzl (ghoelzl@gmail.com)
#
# This file is part of OpenMagnifier
#
# OpenMagnifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenMagnifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMagnifier.  If not, see <http://www.gnu.org/licenses/>.

import ConfigParser

class Config:
    CONFIG_FILE = "openmagnifier.cfg"
    
    def read(self, section_name):
        self.init()    
        self.config.read(Config.CONFIG_FILE)
        return self.config._sections[section_name]
        
    def init(self):
        self.config = ConfigParser.RawConfigParser()    
            
    def write_dictionary(self, section_name, dictionary):
        self.config.add_section(section_name)    
        for key, value in dictionary.items():
            self.config.set(section_name, key, value)
        
    def write_finish(self):
        with open(Config.CONFIG_FILE, 'wb') as configfile:
            self.config.write(configfile)
