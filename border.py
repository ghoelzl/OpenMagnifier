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

import pygame

class Border:
    
    def __init__(self):
        self.width = 0.25
        self.offset = 0.0

    def set_size(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.new_surface()
        
    def new_surface(self):        
        self.surface = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA)
        y_pos = int(self.size_y*(0.5+self.offset-self.width/2.0))
        if y_pos > 0:
            self.surface.fill((0,0,0,160),(0,0,self.size_x,y_pos))
        else:
            self.offset = self.width/2.0-0.5    
        y_pos = int(self.size_y*(0.5+self.offset+self.width/2.0))
        if y_pos < self.size_y:            
            self.surface.fill((0,0,0,160),(0,y_pos,self.size_x,self.size_y-1))
        else:     
            self.offset = 0.5-self.width/2.0
        
    def change_width(self, delta):
        self.width += delta
        if self.width < 0.05: 
            self.width = 0.05
        if self.width > 1.0:
            self.width = 1.0
        self.new_surface()
        
    def change_offset(self, delta):
        self.offset += delta
        if (self.width/2.0-self.offset) < -0.5:
            self.offset = self.width/2.0-0.5
        if (self.width/2.0+self.offset) > 0.5:
            self.offset = 0.5-self.width/2.0
        self.new_surface()
        
    def set_config(self, dictionary):
        if dictionary.has_key('width'):
            self.width = float(dictionary['width']);
        if dictionary.has_key('offset'):
            self.offset = float(dictionary['offset']);
            
    def get_config(self):
        values = ({
            'width':self.width, 
            'offset':self.offset
        })
        return values
           
            