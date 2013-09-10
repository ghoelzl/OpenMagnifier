#!/usr/bin/env python

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

import camera
import config
import pygame
import settings
import border

class OpenMagnifier:
    
    MODE_MOVE = 0
    MODE_FOCUS = 1
    MODE_BORDER = 2
    MODE_FILTER = 3
    
    def __init__(self):

        # Init pygame and display
        pygame.init()
        pygame.display.init()
        pygame.mouse.set_visible(0)
        modes = pygame.display.list_modes()
        self.size_x_full = modes[0][0]
        self.size_y_full = modes[0][1]
        self.size_x_window = 1024
        self.size_y_window = self.size_x_window*9/16
        self.border = border.Border()
        self.font = pygame.font.Font(None, 250)
        
        # Keyboard init
        pygame.key.set_repeat(1, 50)
        
        # Default settings
        self.size_x = self.size_x_window
        self.size_y = self.size_y_window
        self.fullscreen = False
        self.cursor_inverted = False
        self.framerate = 10
        
        # Read display configurations
        read_config = config.Config()
        try:
            dictionary = read_config.read("Window")
        except KeyError:
            dictionary = {}   
        self.set_config(dictionary)
        
        # Configure cursor keys
        if self.cursor_inverted == True:
            # simply exchange keys
            (settings.KEYS_MOVE_LEFT, 
            settings.KEYS_MOVE_RIGHT) = (settings.KEYS_MOVE_RIGHT, 
            settings.KEYS_MOVE_LEFT)
            (settings.KEYS_MOVE_UP, 
            settings.KEYS_MOVE_DOWN) = (settings.KEYS_MOVE_DOWN, 
            settings.KEYS_MOVE_UP)

        # Add camera 
        self.camera = camera.Camera()
        self.camera.set_window(self.size_x, self.size_y)   
        self.camera.set_framerate(self.framerate)          

        # Read camera configurations
        try:
            dictionary = read_config.read("Camera")
        except KeyError:
            dictionary = {}   
        self.camera.set_config(dictionary)   
        
        # Read border configurations
        try:
            dictionary = read_config.read("Border")
        except KeyError:
            dictionary = {}   
        self.border.set_config(dictionary)  
        
        # at last we update all config parameters
        self.update_display()     
          
        # Check if camera is attached
        try:
            self.camera.check_camera()
            self.camera.setup_camera()
        except IOError:    
            self.update_message("NO CAMERA")
            self.message_time = -1
            return

        self.camera.update_cropfilter()
            
        if self.fullscreen == True:
            pygame.display.toggle_fullscreen()
                        
        # Init messages        
        self.message_state = 0
        self.mode = OpenMagnifier.MODE_MOVE
        self.update_message()      
                
    def update_display(self):
        flags = 0
        if self.fullscreen:
            self.size_x = self.size_x_full
            self.size_y = self.size_y_full
            flags = pygame.FULLSCREEN | pygame.HWSURFACE
        else:
            self.size_x = self.size_x_window
            self.size_y = self.size_y_window                 
        self.screen = pygame.display.set_mode([self.size_x,self.size_y], flags)                                  
        self.camera.set_window(self.size_x, self.size_y)   
        pygame.display.set_caption("OpenMagnifier")      
        self.border.set_size(self.size_x, self.size_y)     
        self.message_time = 0
    
    def update_message(self, message=None):
        if message == None:
            if self.mode == OpenMagnifier.MODE_MOVE:
                message = "MOVE/ZOOM"
            elif self.mode == OpenMagnifier.MODE_FOCUS:
                message = "FOCUS "
                if self.camera.is_af():
                    message = message + "AF"
                else:
                    message = message + "MF "
            elif self.mode == OpenMagnifier.MODE_BORDER:
                message = "BORDER"
            elif self.mode == OpenMagnifier.MODE_FILTER:
                message = "FILTER"            
        if message != None:
            self.font_surface = self.font.render(message, True, pygame.Color("white"));
        else:
            self.font_surface = None         
        
    def get_config(self):
        values = ({
            'sizex':self.size_x, 
            'sizey':self.size_y,
            'fullscreen':self.fullscreen,
            'cursorinverted':self.cursor_inverted
            })
        return values
        
    def set_config(self, dictionary):
        if dictionary.has_key('sizex'):
            self.size_x = int(dictionary['sizex']);
        if dictionary.has_key('sizey'):
            self.size_y = int(dictionary['sizey']);
        if dictionary.has_key('fullscreen'):
            self.fullscreen = dictionary['fullscreen'] == 'True';
        if dictionary.has_key('cursorinverted'):
            self.cursor_inverted = dictionary['cursorinverted'] == 'True';
        
    def exit(self):
        write_config = config.Config()
        write_config.init()
        write_config.write_dictionary("Window", self.get_config())
        write_config.write_dictionary("Camera", 
             self.camera.get_config())
        write_config.write_dictionary("Border", 
             self.border.get_config())        
        write_config.write_finish()

    def evaluate_key(self, key):    
        if key in settings.KEYS_TOGGLE_MODE:
            self.mode = self.mode + 1
            if self.mode == 4:
                self.mode = 0
            self.message_time = 0   
            
        if key in settings.KEYS_FULLSCREEN:
            self.fullscreen = not self.fullscreen
            self.update_display()             

        if self.mode == OpenMagnifier.MODE_MOVE:
            if key in settings.KEYS_MOVE_LEFT:
                self.camera.change_view(camera.Camera.MOVE_LEFT)
            elif key in settings.KEYS_MOVE_RIGHT:
                self.camera.change_view(camera.Camera.MOVE_RIGHT)
            elif key in settings.KEYS_MOVE_UP:
                self.camera.change_view(camera.Camera.MOVE_UP)
            elif key in settings.KEYS_MOVE_DOWN:    
                self.camera.change_view(camera.Camera.MOVE_DOWN)
            elif key in settings.KEYS_ZOOM_IN:
                self.camera.change_view(camera.Camera.ZOOM_IN)
            elif key in settings.KEYS_ZOOM_OUT:    
                self.camera.change_view(camera.Camera.ZOOM_OUT)
            elif key in (settings.KEYS_CENTER + settings.KEYS_RESET):
                self.camera.reset_view() 
            elif key in settings.KEYS_ENTER:
                self.camera.change_view(camera.Camera.MOVE_HOME)


        elif self.mode == OpenMagnifier.MODE_FOCUS:
            if key in (settings.KEYS_MOVE_LEFT + settings.KEYS_MOVE_DOWN):
                if self.camera.is_af():
                    self.camera.toggle_af()
                else:    
                    self.camera.change_focus(-10)
            elif key in (settings.KEYS_MOVE_RIGHT + settings.KEYS_MOVE_UP):
                if self.camera.is_af():
                    self.camera.toggle_af()
                else:    
                    self.camera.change_focus(10)
            elif key in (settings.KEYS_CENTER + settings.KEYS_AUTOFOCUS):
                    self.camera.toggle_af()
                    self.message_time = 0
                        
        elif self.mode == OpenMagnifier.MODE_BORDER:
            if key in settings.KEYS_MOVE_LEFT:
                self.border.change_width(-0.05)
            elif key in settings.KEYS_MOVE_RIGHT:
                self.border.change_width(0.05)
            elif key in settings.KEYS_MOVE_UP:
                self.border.change_offset(-0.05)
            elif key in settings.KEYS_MOVE_DOWN:    
                self.border.change_offset(0.05)
            
        elif self.mode == OpenMagnifier.MODE_FILTER:
            if key in settings.KEYS_MOVE_LEFT:
                self.camera.change_colorfilter(1)
            elif key in settings.KEYS_MOVE_RIGHT:
                self.camera.change_colorfilter(-1)
            elif key in settings.KEYS_CENTER:
                self.camera.change_colorfilter(0)                                

        self.update_message()
        self.camera.update_cropfilter()
        
    def event_handler(self, widget, event):
        self.size_x, self.size_y = self.window.get_size()
        if self.camera_player != None:
            self.camera_player.set_window(self.size_x, self.size_y)
            
    def update(self):
        image = self.camera.get_image()        
        self.screen.blit(image, ( 0, 0 ) )
        self.screen.blit(self.border.surface, (0,0))    
        if self.font_surface != None:
            if self.message_time < 30:
                width = self.font_surface.get_width()
                self.screen.blit(self.font_surface, ((self.screen.get_width()-width)/2, 0 ) )
        if self.message_time >= 0:
            self.message_time = self.message_time + 1                                   
        pygame.display.flip()            
            
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key in settings.KEYS_QUIT:
                        running = False
                        break
                    self.evaluate_key(event.key)   
            self.update()        
            clock.tick(self.framerate)
        self.exit()
    
magnifier = OpenMagnifier()
magnifier.run()
    

